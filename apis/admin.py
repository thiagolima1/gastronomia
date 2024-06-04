from django.contrib import admin
from apis.models import *

@admin.register(ReceitaIngrediente)
class ReceitaIngredienteAdmin(admin.ModelAdmin):
    list_display = (
        'receita',
        'produto',
        'quantidade',
    )

@admin.register(TipoCulinaria)
class TipoCulinariaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',

    )


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'tipo',


    )


@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = (
        'descricao',

    )


@admin.register(Produto)
class ProdutoMedidaAdmin(admin.ModelAdmin):
    list_display = (
        'quantidade',
        'unidade',


    )


@admin.register(Preco)
class PrecoAdmin(admin.ModelAdmin):
    list_display = (
        'produto',
        'data_cotacao',
        'valor',

    )


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = (
        'nome',


    )


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',

    )


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = (
        'nome',

    )


@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = (
        'data_emissao',
        'valor',

    )


@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'localizacao',

    )


@admin.register(AulaReceita)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = (
        'aula',
        'receita',
        'qtd_receita',

    )


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = (
        'data',
        'turno',
        'disciplina',
        'professor',
        'laboratorio',
        'qtd_aluno',
        'confirmada',


    )


@admin.register(Movimento)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = (
        'produto',
        'tipo',
        'quantidade',


    )


@admin.register(ItemNotaFiscal)
class ItemNotaFiscalAdmin(admin.ModelAdmin):
    list_display = (
        'notafiscal',
        'produto',
        'preco_unitario',
        'quantidade',

    )