from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('receitasingrediente', ReceitaIngredienteViewSet)
router.register('tiposculinaria', TipoCulinariaViewSet)
router.register('receitas', ReceitaViewSet)
router.register('unidadesmedida', UnidadeMedidaViewSet)
router.register('produtos', ProdutoViewSet)
router.register('precos', PrecoViewSet)
router.register('professores', ProfessorViewSet)
router.register('disciplinas', DisciplinaViewSet)
router.register('fornecedores', FornecedorViewSet)
router.register('laboratorios', LaboratorioViewSet)
router.register('receitasaula', AulaReceitaViewSet)
router.register('aulas', AulaViewSet)
router.register('movimentos', MovimentoViewSet)
router.register('notasfiscais', NotaFiscalViewSet)
router.register('itensnotasfiscais', ItemNotaFiscalViewSet)


urlpatterns = [
    path("", index),
    path('custosdiario/', CustoDiarioApiView.as_view(), name='custosdiario'),
    path('posicaoestoque/', PosicaoEstoqueApiView.as_view(), name='posicaoestoque'),
    path('confirmaaula/<int:pk>/', ConfirmaAulaApiView.as_view(), name='confirmaaula'),
    path('cancelaaula/<int:pk>/', CancelaAulaApiView.as_view(), name='cancelaaula'),
    path('detalhesaula/<int:pk>/', DetalhesAulaApiView.as_view(), name='detalhesaula'),
    path('necessidadecompra/', NecessidadeCompraApiView.as_view(), name='necessidadecompra'),
    path('entradanota/', EntradaNotaFiscalApiView.as_view(), name='entradanota'),
]
