from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from escola.models import Aluno, Curso, Matricula
from escola.serializer import AlunoSerializer, AlunoSerializerV2, CursoSerializer, MatriculaSerializer, ListaMatriculasAlunoSerializer, ListaAlunosMatriculadosSerializer


def insert_data(instance, request):
    serializer = instance.serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        instance_id = str(serializer.data['id'])
        response['Location'] = request.build_absolute_uri() + instance_id
        return response


class AlunosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os alunos e alunas"""
    queryset = Aluno.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return AlunoSerializerV2
        else:
            return AlunoSerializer


class CursosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os cursos"""
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def create(self, request):
        return insert_data(self, request)


class MatriculaViewSet(viewsets.ModelViewSet):
    """Listando todas as matrículas"""
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    http_method_names = ['get', 'post', 'put', 'patch']

    def create(self, request):
        return insert_data(self, request)

    @method_decorator(cache_page(20))
    def dispatch(self, *args, **kwargs):
        return super(MatriculaViewSet, self).dispatch(*args, **kwargs)


class ListaMatriculasAluno(generics.ListAPIView):
    """Listando as matrículas de um aluno ou aluna"""
    def get_queryset(self):
        queryset = Matricula.objects.filter(aluno_id=self.kwargs['pk'])
        return queryset
    serializer_class = ListaMatriculasAlunoSerializer


class ListaAlunosMatriculados(generics.ListAPIView):
    """Listando alunos e alunas matriculados em um curso"""
    def get_queryset(self):
        queryset = Matricula.objects.filter(curso_id=self.kwargs['pk'])
        return queryset
    serializer_class = ListaAlunosMatriculadosSerializer
