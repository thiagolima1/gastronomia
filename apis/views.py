from datetime import date, timedelta
from dateutil.parser import parse
from django.db import transaction
from django.utils.dateparse import parse_date
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .funcoes import *
from django.shortcuts import render


def index(request):
    context = {"dados":'Apis para o sistema de Controle de Produtos paras as aulas de Gastronomia'}
    return render(request, 'index.html', context)


class ReceitaIngredienteViewSet(viewsets.ModelViewSet):
    queryset = ReceitaIngrediente.objects.filter(ativo=True)
    serializer_class = ReceitaIngredienteSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class TipoCulinariaViewSet(viewsets.ModelViewSet):
    queryset = TipoCulinaria.objects.filter(ativo=True)
    serializer_class = TipoCulinariaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class ReceitaViewSet(viewsets.ModelViewSet):
    queryset = Receita.objects.filter(ativo=True)
    serializer_class = ReceitaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class UnidadeMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadeMedida.objects.filter(ativo=True)
    serializer_class = UnidadeMedidaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.filter(quantidade__gt=0) | Produto.objects.filter(ativo=True)
    serializer_class = ProdutoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class PrecoViewSet(viewsets.ModelViewSet):
    queryset = Preco.objects.filter(ativo=True)
    serializer_class = PrecoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.filter(ativo=True)
    serializer_class = ProfessorSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class DisciplinaViewSet(viewsets.ModelViewSet):
    """
    Cadastro de Disciplinas
    """
    queryset = Disciplina.objects.filter(ativo=True)
    serializer_class = DisciplinaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.filter(ativo=True)
    serializer_class = FornecedorSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class NotaFiscalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotaFiscal.objects.filter(ativo=True)
    serializer_class = NotaFiscalSerializer


class ItemNotaFiscalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemNotaFiscal.objects.filter(ativo=True)
    serializer_class = ItemNotaFicalSerializer


class LaboratorioViewSet(viewsets.ModelViewSet):
    queryset = Laboratorio.objects.filter(ativo=True)
    serializer_class = LaboratorioSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class AulaReceitaViewSet(viewsets.ModelViewSet):
    queryset = AulaReceita.objects.filter(ativo=True)
    serializer_class = AulaReceitaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()


class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.filter(ativo=True)
    serializer_class = AulaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.validated_data.pop('confirmada', None)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovimentoViewSet(viewsets.ModelViewSet):
    queryset = Movimento.objects.filter(ativo=True)
    serializer_class = MovimentoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()

    def create(self, request, *args, **kwargs):
        produto_id = request.data['produto']
        quantidade = request.data['quantidade']
        tipo = request.data['tipo']
        user = str(self.request.user)
        if tipo.upper() == 'S':
            return Response('Saída de prodúto só por confirmação de aula', status=status.HTTP_400_BAD_REQUEST)
        if tipo.upper() == 'E':
            return Response('Entrada de prodúto deve ser feita pela nota fiscal ou po devolução de material', status=status.HTTP_400_BAD_REQUEST)
        movimenta = movimentaproduto(produto_id, tipo, quantidade, user)
        if movimenta:
            return Response('Movimentação realizada com sucesso', status=status.HTTP_201_CREATED)
        else:
            return Response('Falha ao movimentar o produto', status=status.HTTP_400_BAD_REQUEST)


class CustoDiarioApiView(APIView):
    """
    Custo por dia de aula prática
    """

    def get(self, request):
        aulas = Aula.objects.all()
        df_aula = read_frame(aulas)
        aulas_receita = AulaReceita.objects.filter(aula__in=aulas, ativo=True)
        df_aulas_receita = read_frame(aulas_receita)
        df_aulas_receita['id_aula'] = aulas_receita.values_list('aula_id', flat=True)
        df_aulas_receita['id_receita'] = aulas_receita.values_list('receita_id', flat=True)
        df_custo = pd.merge(df_aula, df_aulas_receita, left_on=['id'],
                            right_on=['id_aula'], how='left')
        colunas = ['data', 'qtd_receita', 'id_receita']
        df_custo = df_custo[colunas]
        del aulas
        del aulas_receita
        del df_aula
        del df_aulas_receita
        receitas_ingrediente = ReceitaIngrediente.objects.all()
        df_receitas_ingrediente = read_frame(receitas_ingrediente)
        df_receitas_ingrediente['id_produto'] = receitas_ingrediente.values_list('produto_id', flat=True)
        df_receitas_ingrediente['id_receita'] = receitas_ingrediente.values_list('receita_id', flat=True)
        df_custo = pd.merge(df_custo, df_receitas_ingrediente, left_on=['id_receita'],
                            right_on=['id_receita'], how='left')
        df_custo['qtd'] = df_custo['qtd_receita'] * df_custo['quantidade']
        colunas = ['data', 'qtd', 'id_produto']
        df_custo = df_custo[colunas]
        df_custo = df_custo.groupby(['data', 'id_produto'])['qtd'].aggregate(['sum'])
        df_custo = df_custo.reset_index()
        del receitas_ingrediente
        del df_receitas_ingrediente
        precos = Preco.objects.all()
        df_precos = precomedio(precos)
        df_custo = pd.merge(df_custo, df_precos, left_on=['id_produto'],
                            right_on=['id_prod'], how='left')
        df_custo['sum'] = df_custo['sum'].astype(float)
        df_custo['mean'] = df_custo['mean'].astype(float)
        df_custo['custo'] = df_custo['sum'] * df_custo['mean']
        df_custo = df_custo.groupby(['data'])['custo'].aggregate(['sum'])
        df_custo = df_custo.reset_index()
        df_custo['sum'] = round(df_custo['sum'], 2)
        df_custo.columns = ['data', 'valor']
        serializer = CustoDiarioSerializer(df_custo.to_dict(orient='records'), many=True)
        return Response(serializer.data)


class PosicaoEstoqueApiView(APIView):
    """
    Posição do Estque
    """
    def get(self, request):
        df_estoque = posicaoestoque()
        colunas = ['nome', 'unidade', 'quantidade', 'preco_medio', 'total']
        df_estoque = df_estoque[colunas]
        serializer = PosicaoEstoqueSerializer(df_estoque.to_dict(orient='records'), many=True)
        return Response(serializer.data)


class NecessidadeCompraApiView(APIView):
    def get(self, request, format=None):
        data = request.query_params.get('data')
        confirmada = request.query_params.get('data')
        hoje = date.today()
        if data is None:
            data = hoje + timedelta(30)
        else:
            try:
                data = parse(data, dayfirst=True).date()
                if data < hoje:
                    return Response("Data não pode ser anterior a data atual", status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response("Data inválida", status=status.HTTP_400_BAD_REQUEST)
        if confirmada == None:
            confirmada = 'N'
        if confirmada.upper() == 'S':
            aulas = Aula.objects.filter(data__range=(hoje, data), confirmada=True)
        elif confirmada.upper() == 'N':
            aulas = Aula.objects.filter(data__range=(hoje, data), confirmada=False)
        else:
            return Response('confirmada deve ser S ou N', status=status.HTTP_400_BAD_REQUEST)
        df_aulas = read_frame(aulas)
        df_aulas_produtos = pd.DataFrame()
        for dado in df_aulas.itertuples():
            df_aula_produtos = produtosaula(dado.id)
            df_aulas_produtos = pd.concat([df_aulas_produtos, df_aula_produtos])
        colunas = ['id_produto', 'qtd_ingrediente']
        df_aulas_produtos = df_aulas_produtos[colunas]
        df_aulas_produtos = df_aulas_produtos.groupby(['id_produto'])['qtd_ingrediente'].aggregate(['sum'])
        df_aulas_produtos = df_aulas_produtos.reset_index()
        df_estoque = posicaoestoque(list(df_aulas_produtos.id_produto))
        df_estoque = pd.merge(df_estoque, df_aulas_produtos, left_on=['id'],
                              right_on=['id_produto'], how='left')
        df_estoque.fillna(0, inplace=True)
        df_estoque['necessidade'] = df_estoque['quantidade'] - df_estoque['sum']
        df_estoque['custo'] = df_estoque['necessidade'] * df_estoque['preco_medio']
        df_necessidade = df_estoque.query('necessidade < 0')
        df_necessidade['necessidade'] = df_necessidade['necessidade'] * -1
        df_necessidade['custo'] = df_necessidade['custo'] * -1
        colunas = ['nome', 'unidade', 'necessidade', 'custo']
        df_necessidade = df_necessidade[colunas]
        df_necessidade.columns = ['produto', 'unidade', 'quntidade', 'custo']
        serializer = NecessidadeCompraSerializer(df_necessidade.to_dict(orient='records'), many=True)
        return Response(serializer.data)


class DetalhesAulaApiView(generics.RetrieveAPIView):
    serializer_class = AulaSerializer
    queryset = Aula.objects.select_related(
            'disciplina',
            'professor',
            'laboratorio',
        )


    def get(self, request, *args, **kwargs):
        aula = self.get_object()

        # ************************************
        # Informações da aula
        # ************************************
        dados = aula.__dict__
        df_aula = pd.DataFrame([dados])
        df_aula['professor'] = aula.professor
        df_aula['disciplina'] = aula.disciplina
        df_aula['laboratorio'] = aula.laboratorio
        colunas = ['id', 'data', 'turno', 'qtd_aluno', 'confirmada', 'professor',
                   'disciplina', 'laboratorio']
        df_aula = df_aula[colunas]
        del dados
        df_receitas = receitasaula(aula.id)
        df_produto = produtosaula(aula.id)
        colunas = ['ingrediente', 'unidade', 'qtd_ingrediente', 'custo']
        df_produto = df_produto[colunas]
        colunas = ['receita', 'tipoculinaria', 'qtd_receita']
        df_receitas = df_receitas[colunas]
        dict_receita = df_receitas.to_dict(orient='records')
        dict_produto = df_produto.to_dict(orient='records')
        item_receita = ReceitaItemSerializer(dict_receita, many=True)
        item_produto = ProdutoItemSerializer(dict_produto, many=True)
        detalhe = df_aula.to_dict(orient='records')
        detalhe[0]['receitas'] = item_receita.data
        detalhe[0]['produtos'] = item_produto.data
        serializer = DetalheAulaSerializer(detalhe[0])
        return Response(serializer.data)


class ConfirmaAulaApiView(generics.UpdateAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_update(self, serializer):
        serializer.validated_data['usuario'] = str(self.request.user)
        serializer.save()

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        aula = self.get_object()
        if aula.confirmada:
            return Response("Aula já confirmada", status=status.HTTP_400_BAD_REQUEST)
        produtos = produtosaula(aula.id)
        for dado in produtos.itertuples():
            movimento = movimentaproduto(dado.id_produto, 'S', dado.qtd_ingrediente, self.request.user)
            movimento_dict = {"produto": dado.id_produto, "tipo": "S", "quantidade": dado.qtd_ingrediente}
            movimento_serializer = MovimentoSerializer(data=movimento_dict)
            if movimento_serializer.is_valid(raise_exception=True):
                movimento_serializer.validated_data['usuario'] = str(self.request.user)
                movimento_serializer.save()


        aula.confirmada = True
        aula.usuario = self.request.user
        aula.save()
        return Response("Aula confirmada com sucesso", status=status.HTTP_200_OK)


class CancelaAulaApiView(generics.UpdateAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        aula = self.get_object()
        if not aula.confirmada:
            return Response("Aula não confirmada", status=status.HTTP_400_BAD_REQUEST)
        produtos = produtosaula(aula.id)
        for dado in produtos.itertuples():
            movimento = movimentaproduto(dado.id_produto, 'E', dado.qtd_ingrediente, self.request.user)
            movimento_dict = {"produto": dado.id_produto, "tipo": "E", "quantidade": dado.qtd_ingrediente}
            movimento_serializer = MovimentoSerializer(data=movimento_dict)
            if movimento_serializer.is_valid(raise_exception=True):
                movimento_serializer.validated_data['usuario'] = str(self.request.user)
                movimento_serializer.save()

        aula.confirmada = False
        aula.usuario = self.request.user
        aula.save()
        serializer = AulaSerializer(aula)
        return Response("Aula cancelada com sucesso", status=status.HTTP_200_OK)


class EntradaNotaFiscalApiView(generics.CreateAPIView):
    queryset = None
    serializer_class = EntradaNotaFiscalSerializer

    def create(self, request, *args, **kwargs):
        try:
            hoje = date.today()
            data_emissao = parse_date(request.data.get('notafiscal', {}).get('data_emissao'))
            if data_emissao and data_emissao > hoje:
                return Response("Não é possível cadastrar Nota Fiscal no Futuro",
                                status=status.HTTP_400_BAD_REQUEST)
            produtos = request.data.get('produtos', [])
            if len(produtos) == 0:
                return Response("Tem que ser informado ao menos um produto",
                                status=status.HTTP_400_BAD_REQUEST)
            prodid = [produto["produto"] for produto in produtos]
            prods = Produto.objects.filter(id__in = prodid)
            prods1 = prods.values_list('id', flat=True)
            prods1 = set(prods1)
            prodid = set(prodid)
            if len(prodid - prods1) != 0:
                return Response("Os produtos" + str(prodid - prods1) + "não estão cadastrados",
                                status=status.HTTP_400_BAD_REQUEST)
            notafiscal = request.data.get('notafiscal')
            forn_id = notafiscal['fornecedor']
            fornecedor = Fornecedor.objects.filter(id=forn_id).count()
            if fornecedor == 0:
                return Response("Fornecedor não  cadastrado",
                                status=status.HTTP_400_BAD_REQUEST)
            valortotal = sum([produto["quantidade"] * produto["preco_unitario"] for produto in produtos])
            nota_serializer = NotaFiscalSerializer(data=request.data.get('notafiscal', {}))
            if nota_serializer.is_valid(raise_exception=True):
                with transaction.atomic():
                    nota_serializer.validated_data['valor'] = valortotal
                    nota_serializer.validated_data['usuario'] = str(self.request.user)
                    nota = nota_serializer.save()
                    for produto in produtos:
                        produto['notafiscal'] = nota.id
                        item_serializer = ItemNotaFicalSerializer(data=produto)
                        if item_serializer.is_valid(raise_exception=True):
                            item_serializer.validated_data['usuario'] = str(self.request.user)
                            item_serializer.save()
                            movimento = movimentaproduto(produto['produto'], 'E',
                                                         produto['quantidade'],
                                                         str(self.request.user))
                        preco_dict = {"produto": produto['produto'], "data_cotacao": data_emissao,
                                      "valor": produto['preco_unitario']}
                        preco_serializer = PrecoSerializer(data=preco_dict)
                        if preco_serializer.is_valid(raise_exception=True):
                            preco_serializer.validated_data['usuario'] = str(self.request.user)
                            preco_serializer.save()
                        movimento_dict = {"produto": produto['produto'], "tipo": "E", "quantidade": produto['quantidade']}
                        movimento_serializer = MovimentoSerializer(data=movimento_dict)
                        if movimento_serializer.is_valid(raise_exception=True):
                            movimento_serializer.validated_data['usuario'] = str(self.request.user)
                            movimento_serializer.save()
                    return Response("Nota Fiscal criada com sucesso", status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
