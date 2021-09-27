from rest_framework.test import APITestCase
from rest_framework import status
from escola.models import Curso
from django.urls import reverse


class CursoTestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse('Cursos-list')
        self.curso_1 = Curso.objects.create(
            codigo_curso='CTT1', descricao='Curso Teste 1', nivel='B')
        self.curso_2 = Curso.objects.create(
            codigo_curso='CTT2', descricao='Curso Teste 2', nivel='A')

    # def test_gerador_falha(self):
    #     self.fail('Este teste falhou de propósito. Não se preocupe!')

    def test_requisicao_get_para_listar_cursos(self):
        """Teste para verificar se a requisição GET lista os cursos corretamente"""
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_post_para_criar_curso(self):
        """Teste para verificar se a requisição POST cria um curso corretamente"""
        dados_do_curso = {
            'codigo_curso': 'CTT3',
            'descricao': 'Curso Teste 3',
            'nivel': 'I'
        }
        response = self.client.post(self.list_url, data=dados_do_curso)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_requisicao_delete_para_deletar_curso(self):
        """Teste para verificar se a requisição DELETE realmente não é permitida"""
        response = self.client.delete('/cursos/1/')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_requisicao_put_para_atualizar_curso(self):
        """Teste para verificar se a requisição PUT atualiza um curso"""
        dados_do_curso = {
            'codigo_curso': 'CTT1',
            'descricao': 'Curso Teste 1 atualizado',
            'nivel': 'B'
        }
        response = self.client.put('/cursos/1/', data=dados_do_curso)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
