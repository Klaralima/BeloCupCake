"""Execute da pasta backend: python -m unittest discover -s tests -v.

Os testes não abrem conexão com MySQL nem alteram dados reais.
"""
import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

for chave, valor in {
    'DB_USER': 'teste', 'DB_PASSWORD': 'teste', 'DB_HOST': '127.0.0.1',
    'DB_PORT': '3306', 'DB_NAME': 'teste', 'JWT_SECRET_KEY': 'chave-apenas-para-testes-' * 3,
}.items():
    os.environ.setdefault(chave, valor)

from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.database import obter_sessao
from app.dependencies import obter_usuario_atual
from app.routers import entregas, regioes
from app.services.pedido import buscar_pedido_entregador


class ConsultasFrontendTest(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        self.app.include_router(entregas.router)
        self.app.include_router(regioes.router)
        self.sessao = MagicMock()
        self.app.dependency_overrides[obter_sessao] = lambda: self.sessao
        self.client = TestClient(self.app)

    def perfil(self, perfil):
        self.app.dependency_overrides[obter_usuario_atual] = lambda: SimpleNamespace(id=7, perfil=perfil)

    def test_sem_login_retorna_401(self):
        self.assertEqual(self.client.get('/entregas/1').status_code, 401)
        self.assertEqual(self.client.get('/admin/regioes').status_code, 401)

    def test_cliente_nao_acessa_consultas_restritas(self):
        self.perfil('CLIENTE')
        self.assertEqual(self.client.get('/entregas/1').status_code, 403)
        self.assertEqual(self.client.get('/admin/regioes').status_code, 403)

    def test_entregador_nao_acessa_regioes_admin(self):
        self.perfil('ENTREGADOR')
        self.assertEqual(self.client.get('/admin/regioes').status_code, 403)

    def test_entrega_de_outro_entregador_retorna_404(self):
        self.perfil('ENTREGADOR')
        with patch.object(entregas, 'buscar_pedido_entregador', return_value=None) as buscar:
            self.assertEqual(self.client.get('/entregas/42').status_code, 404)
            buscar.assert_called_once_with(self.sessao, 42, 7)

    def test_consulta_sql_exige_pedido_e_entregador(self):
        self.sessao.scalar.return_value = None
        self.assertIsNone(buscar_pedido_entregador(self.sessao, 42, 7))
        consulta = self.sessao.scalar.call_args.args[0]
        sql = str(consulta.compile(compile_kwargs={'literal_binds': True}))
        self.assertIn('pedido.id = 42', sql)
        self.assertIn('entrega.entregador_id = 7', sql)

    def test_admin_lista_regioes_com_paginacao(self):
        self.perfil('ADMINISTRADOR')
        with patch.object(regioes, 'listar_regioes', return_value=[]) as listar:
            resposta = self.client.get('/admin/regioes?limite=10&deslocamento=20')
            self.assertEqual(resposta.status_code, 200)
            self.assertEqual(resposta.json(), [])
            listar.assert_called_once_with(self.sessao, 10, 20)
        self.assertEqual(self.client.get('/admin/regioes?limite=101').status_code, 422)

    def test_rota_estatica_minhas_nao_e_tratada_como_id(self):
        self.perfil('ENTREGADOR')
        with patch.object(entregas, 'listar_minhas_entregas', return_value=[]):
            self.assertEqual(self.client.get('/entregas/minhas').status_code, 200)


if __name__ == '__main__':
    unittest.main()
