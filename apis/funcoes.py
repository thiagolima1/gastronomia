import pandas as pd
from django_pandas.io import read_frame
from apis.models import AulaReceita, Receita, ReceitaIngrediente, Produto, Preco
from apis.serializers import ProdutoSerializer


def ultimascinco(group):
    """

    :param group: coluna de agrupamento
    :return: as 5 maiores de caga agrupamento
    """
    return group.head(5)


def precomedio(precos):
    df_precos = read_frame(precos)
    df_precos['produto'] = precos.values_list('produto_id', flat=True)
    df_precos = df_precos.sort_values(by='data_cotacao', ascending=False)
    df_precos = df_precos.groupby('produto').apply(ultimascinco)
    df_precos.columns = ['id', 'data_criacao', 'data_ateracao', 'ativo', 'usuario', 'id_prod', 'data_cotacao', 'valor']
    df_precos = df_precos.groupby(['id_prod'])['valor'].aggregate(['mean'])
    df_precos = df_precos.reset_index()
    return df_precos

def receitasaula(aula_id):
    # ************************************
    # Receitas da aula
    # ************************************
    aulas_receita = AulaReceita.objects.filter(aula_id=aula_id, ativo=True)
    df_aulas_receita = read_frame(aulas_receita)
    df_aulas_receita['id_receita'] = aulas_receita.values_list('receita_id', flat=True)
    colunas = ['qtd_receita', 'id_receita']
    df_aulas_receita = df_aulas_receita[colunas]
    receitas = Receita.objects.select_related(
        'tipo',
    ).filter(pk__in=aulas_receita.values_list('receita_id', flat=True))
    df_receitas = read_frame(receitas)
    colunas = ['id', 'nome', 'tipo']
    df_receitas = df_receitas[colunas]
    df_receitas.columns = ['id', 'receita', 'tipoculinaria']
    df_receitas = pd.merge(df_receitas, df_aulas_receita, right_on=['id_receita'],
                           left_on=['id'], how='inner')
    colunas = ['id_receita', 'receita', 'tipoculinaria', 'qtd_receita']
    df_receitas = df_receitas[colunas]
    return df_receitas

def produtosaula(aula_id):
    # ************************************
    # Ingredientes usados na aula
    # ************************************
    df_receitas = receitasaula(aula_id)
    receita_produto = ReceitaIngrediente.objects.filter(receita_id__in=df_receitas.id_receita, ativo=True)
    df_receita_produto = read_frame(receita_produto)
    df_receita_produto['id_produto'] = receita_produto.values_list('produto_id', flat=True)
    colunas = ['quantidade', 'id_produto']
    df_receita_produto = df_receita_produto[colunas]
    df_receita_produto = df_receita_produto.groupby(['id_produto'])['quantidade'].aggregate(['sum'])
    df_receita_produto = df_receita_produto.reset_index()
    produtos = Produto.objects.select_related(
        'unidade',
    ).filter(id__in=receita_produto.values_list('produto_id', flat=True))
    df_produto = read_frame(produtos)
    colunas = ['id', 'nome', 'unidade']
    df_produto = df_produto[colunas]
    df_produto = pd.merge(df_produto, df_receita_produto, left_on=['id'],
                          right_on=['id_produto'], how='inner')
    colunas = ['nome', 'unidade', 'id_produto', 'sum']
    df_produto = df_produto[colunas]
    df_produto.columns = ['ingrediente', 'unidade', 'id_produto', 'qtd_ingrediente']
    precos = Preco.objects.filter(produto_id__in=produtos)
    df_precos = precomedio(precos)
    df_produto = pd.merge(df_produto, df_precos, left_on=['id_produto'],
                          right_on=['id_prod'], how='left')
    df_produto.fillna(0, inplace=True)
    df_produto['qtd_ingrediente'] = df_produto['qtd_ingrediente'].astype(float)
    df_produto['mean'] = df_produto['mean'].astype(float)
    df_produto['custo'] = df_produto['qtd_ingrediente'] * df_produto['mean']
    colunas = ['ingrediente', 'unidade', 'qtd_ingrediente', 'custo', 'id_produto']
    df_produto = df_produto[colunas]
    return df_produto

def movimentaproduto(produto_id, tipo, quantidade, user):
    produto_queryset = Produto.objects.filter(id=produto_id)
    quantidade_entrada = float(quantidade)
    quantidade_produto = produto_queryset[0].quantidade
    if tipo in ['E', 'A', 'D']:
        quantidade_produto = float(quantidade_produto) + float(quantidade_entrada)
    else:
        quantidade_produto = float(quantidade_produto) - float(quantidade_entrada)
    produto_serializer = ProdutoSerializer(produto_queryset, many=True)
    produto_data = produto_serializer.data
    produto_data[0]['quantidade'] = quantidade_produto
    produto = Produto.objects.get(id=produto_id)
    produto.quantidade = produto_data[0]['quantidade']
    produto.usuario = user
    produto.save()
    return True

def posicaoestoque(produto=None):
    if produto == None:
        produtos = Produto.objects.all()
    else:
        produtos = Produto.objects.filter(id__in=produto)
    df_produtos = read_frame(produtos)
    precos = Preco.objects.all()
    df_precos = precomedio(precos)
    df_produtos['id'] = df_produtos['id'].astype(int)
    df_precos['id_prod'] = df_precos['id_prod'].astype(int)
    df_estoque = pd.merge(df_produtos, df_precos, left_on=['id'],
                          right_on=['id_prod'], how='left')
    df_estoque['mean'] = df_estoque['mean'].astype(float)
    df_estoque['quantidade'] = df_estoque['quantidade'].astype(float)
    df_estoque['valor'] = df_estoque['mean'] * df_estoque['quantidade']
    colunas = ['id', 'data_criacao', 'data_ateracao', 'ativo', 'usuario', 'nome',
               'quantidade', 'unidade', 'id_prod', 'preco_medio', 'total']
    df_estoque.columns = colunas
    colunas = ['nome', 'unidade', 'quantidade', 'preco_medio', 'total', 'id']
    df_estoque = df_estoque[colunas]
    df_estoque['preco_medio'] = round(df_estoque['preco_medio'], 2)
    df_estoque['total'] = round(df_estoque['total'], 2)
    return df_estoque
