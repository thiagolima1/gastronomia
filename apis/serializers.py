from rest_framework import serializers
from .models import *

class ReceitaIngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceitaIngrediente
        fields = '__all__'
        read_only_fields = ['ativo']

class TipoCulinariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCulinaria
        fields = '__all__'
        read_only_fields = ['ativo']

class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = '__all__'
        read_only_fields = ['ativo']

class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = '__all__'
        read_only_fields = ['ativo']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        read_only_fields = ['ativo']

class PrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preco
        fields = '__all__'
        read_only_fields = ['ativo']

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'
        read_only_fields = ['ativo']

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'
        read_only_fields = ['ativo']

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'
        read_only_fields = ['ativo']

class NotaFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaFiscal
        fields = '__all__'
        read_only_fields = ['ativo']

class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorio
        fields = '__all__'
        read_only_fields = ['ativo']


class AulaReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AulaReceita
        fields = '__all__'
        read_only_fields = ['ativo']

class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = '__all__'
        read_only_fields = ['ativo']


class MovimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimento
        fields = '__all__'
        read_only_fields = ['ativo']

class MovimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimento
        fields = '__all__'
        read_only_fields = ['ativo']


