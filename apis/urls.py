from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('receitaingrediente', ReceitaIngredienteViewSet)
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
]


