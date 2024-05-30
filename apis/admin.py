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