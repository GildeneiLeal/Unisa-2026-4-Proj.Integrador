import json
import os
import webbrowser
from fasthtml.common import *

# Inicializa o aplicativo FastHTML com Pico CSS habilitado e folha de estilo padrao.css
app, retorno = fast_app(
    pico=True,
    hdrs=(Link(rel="stylesheet", href="/static/padrao.css"),),
)

# Categorias
CATEGORIAS_VALIDAS = ["salario", "alimentacao", "vestuario", "saude", "transporte", "investimento", "imposto"]
TIPOS_VALIDOS = ["receita", "despesa"]

# Dicionário padronizado com mensagens de alerta de erro
MENSAGENS = {
    "valor_invalido": "O valor digitado deve ser positivo e maior que zero (R$ 0,00).",
    "formato_valor": "Formato de valor numérico inválido. Por exemplo, utilize 50.00.",
    "dominio_invalido": "Categoria ou Tipo de lançamento fora das opções permitidas.",
    "codigo_duplicado": "Já existe um lançamento cadastrado com esse código.",
    "data_invalida": "Data inválida! Verifique o dia, mês ou se o formato é DD/MM/AAAA (ex: 31/10/2026)."
}

# Arquivo de Dados
ARQUIVO_DADOS = "data/finance_data.json"

def garantir_diretorio_e_arquivo():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

def carregar():
    garantir_diretorio_e_arquivo()
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def salvar(transacoes):
    garantir_diretorio_e_arquivo()
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(transacoes, f, ensure_ascii=False, indent=4)

def selection_sort(transacoes, criterio="valor"):
    n = len(transacoes)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if criterio == "valor":
                if transacoes[j]["valor"] < transacoes[min_idx]["valor"]:
                    min_idx = j
            elif criterio == "data":
                data_j = transacoes[j]["data"]
                data_min = transacoes[min_idx]["data"]

                parts_j = data_j.split("/")
                val_j = parts_j[2] + parts_j[1] + parts_j[0] if len(parts_j) == 3 else data_j

                parts_min = data_min.split("/")
                val_min = parts_min[2] + parts_min[1] + parts_min[0] if len(parts_min) == 3 else data_min

                if val_j < val_min:
                    min_idx = j
            elif criterio == "codigo":
                if transacoes[j]["codigo"] < transacoes[min_idx]["codigo"]:
                    min_idx = j
        transacoes[i], transacoes[min_idx] = transacoes[min_idx], transacoes[i]
    return transacoes

def pesquisa_sequencial(transacoes, termo):
    if not termo:
        return transacoes
    termo = termo.lower().strip()
    resultados = []
    for t in transacoes:
        if (termo in t["categoria"].lower() or
            termo in t["tipo"].lower() or
            termo == str(t["codigo"])):
            resultados.append(t)
    return resultados

def pesquisa_binaria_por_codigo(transacoes, codigo_alvo):
    trans_ordenadas = selection_sort(list(transacoes), criterio="codigo")
    baixo = 0
    alto = len(trans_ordenadas) - 1

    while baixo <= alto:
        meio = (baixo + alto) // 2
        atual = trans_ordenadas[meio]["codigo"]
        if atual == codigo_alvo:
            return [trans_ordenadas[meio]]
        elif atual < codigo_alvo:
            baixo = meio + 1
        else:
            alto = meio - 1
    return []

def converter_data_para_comparacao(data_str):
    parts = data_str.strip().split("/")
    if len(parts) == 3:
        return parts[2] + parts[1] + parts[0]
    return ""

# Componente compartilhado do Menu Superior
def criar_menu_superior():
    return Form(
        Button("Cadastrar", type="submit", name="acao", value="cadastrar", style="width: 200px;"),
        " ",
        Button("Listar", type="submit", name="acao", value="listar", style="width: 200px;"),
        " ",
        Button("Buscar", type="submit", name="acao", value="buscar", style="width: 200px;"),
        " ",
        Button("Ranking", type="submit", name="acao", value="ranking", style="width: 200px;"),
        " ",
        Button("Relatório", type="submit", name="acao", value="relatorio", style="width: 200px;"),
        " ",
        method="post",
        action="/navegar",
        cls="menu-superior"
    )

def validar_data(data_str):
    if not data_str:
        return False

    partes = data_str.strip().split("/")
    if len(partes) != 3:
        return False

    dia_str, mes_str, ano_str = partes

    if not (dia_str.isdigit() and mes_str.isdigit() and ano_str.isdigit()):
        return False

    dia = int(dia_str)
    mes = int(mes_str)
    ano = int(ano_str)

    if not (1 <= mes <= 12):
        return False
    if ano < 1900 or ano > 2100:
        return False

    dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    bissexto = (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)
    if bissexto:
        dias_por_mes[2] = 29

    if not (1 <= dia <= dias_por_mes[mes]):
        return False

    return True

@retorno("/")
def get(criterio: str = "valor"):
    # Redireciona a raiz para a rota de navegação
    return RedirectResponse("/navegar?acao=cadastrar", status_code=303)

# Rota centralizadora para direcionar cada botão do menu superior
@retorno("/navegar", methods=["GET", "POST"])
def navegar(acao: str = "cadastrar", criterio_ranking: str = "valor", busca_seq: str = "", busca_bin: str = "", data_inicio: str = "", data_fim: str = "", erro: str = ""):
    menu_superior = criar_menu_superior()

    if acao == "cadastrar":
        transacoes = carregar()
        total_receitas = sum(t["valor"] for t in transacoes if t["tipo"] == "receita")
        total_despesas = sum(t["valor"] for t in transacoes if t["tipo"] == "despesa")
        saldo = total_receitas - total_despesas

        alerta_erro = ""
        if erro in MENSAGENS:
            alerta_erro = Div(
                P(MENSAGENS[erro], style="margin: 0; font-weight: bold; color: #721c24;"),
                style="background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 12px; border-radius: 4px; margin-bottom: 1rem;"
            )

        form_cadastro = Form(
            Fieldset(
                Legend("Novo Lançamento"),
                Div(
                    Label("Data (DD/MM/AAAA):", _for="data"),
                    Input(type="text", id="data", name="data", placeholder="Ex: 25/10/2026", required=True),
                    cls="campo-horizontal"
                ),
                Div(
                    Label("Tipo de Lançamento:", _for="tipo"),
                    Select(
                        Option("Receita", value="receita"),
                        Option("Despesa", value="despesa"),
                        name="tipo", id="tipo"
                    ),
                    cls="campo-horizontal"
                ),
                Div(
                    Label("Categoria:", _for="categoria"),
                    Select(
                        Option("Salário", value="salario"),
                        Option("Alimentação", value="alimentacao"),
                        Option("Vestuário", value="vestuario"),
                        Option("Saúde", value="saude"),
                        Option("Transporte", value="transporte"),
                        Option("Investimento", value="investimento"),
                        Option("Imposto", value="imposto"),
                        name="categoria", id="categoria", required=True
                    ),
                    cls="campo-horizontal"
                ),
                Div(
                    Label("Valor (R$):", _for="valor"),
                    Input(type="number", step="0.01", id="valor", name="valor", placeholder="0.00", required=True),
                    cls="campo-horizontal"
                ),
                Button("Inserir", type="submit", style="width: 200px;")
            ),
            method="post",
            action="/adicionar",
            cls="form_cadastro"
        )

        painel_resumo = Fieldset(
            Div(
                Legend("Resumo Financeiro", style="width: 200px;"),
                P(f"Total Receitas: R$ {total_receitas:.2f}"),
                P(f"Total Despesas: R$ {total_despesas:.2f}"),
                P(f"Saldo Atual: R$ {saldo:.2f}"),
                style="background-color: lightblue; padding: 10px;"
            ),
            cls="painel-resumo"
        )

        tabela_linhas = [
            Tr(Td(str(t["codigo"])), Td(t["data"]), Td(t["tipo"]), Td(t["categoria"]), Td(f"R$ {t['valor']:.2f}"))
            for t in transacoes
        ]

        tabela = Table(
            Thead(Tr(Th("Cód"), Th("Data"), Th("Tipo"), Th("Categoria"), Th("Valor"))),
            Tbody(*tabela_linhas)
        ) if tabela_linhas else P("Nenhum lançamento encontrado ou cadastrado.")

        conteudo = Div(
            H1("Controle Orçamentário Familiar"),
            menu_superior,
            alerta_erro,
            Div(
                form_cadastro,
                painel_resumo,
                cls="painel-principal"
            ),
            H1("Lista de Transações"),
            Hr(),
            tabela,
            cls="container"
        )
        return Titled("Controle Financeiro - Cadastrar", conteudo)

    elif acao == "listar":
        transacoes = carregar()
        tabela_linhas = [Tr(Td(str(t["codigo"])), Td(t["data"]), Td(t["tipo"]), Td(t["categoria"]), Td(f"R$ {t['valor']:.2f}")) for t in transacoes]
        tabela = Table(Thead(Tr(Th("Cód"), Th("Data"), Th("Tipo"), Th("Categoria"), Th("Valor"))), Tbody(*tabela_linhas)) if tabela_linhas else P("Nenhum lançamento cadastrado.")

        conteudo = Div(
            H1("Controle Orçamentário Familiar - Listagem"),
            menu_superior,
            H2("Lista Completa de Transações"),
            tabela,
            A("Voltar ao Início", href="/navegar?acao=cadastrar", role="button", cls="outline"),
            cls="container"
        )
        return Titled("Controle Financeiro - Listar", conteudo)

    elif acao == "buscar":
        transacoes = carregar()

        if busca_seq:
            transacoes = pesquisa_sequencial(transacoes, busca_seq)
        elif busca_bin:
            try:
                cod_alvo = int(busca_bin)
                transacoes = pesquisa_binaria_por_codigo(transacoes, cod_alvo)
            except ValueError:
                transacoes = []

        tabela_busca_linhas = [
            Tr(Td(str(t["codigo"])), Td(t["data"]), Td(t["tipo"]), Td(t["categoria"]), Td(f"R$ {t['valor']:.2f}"))
            for t in transacoes
        ]

        tabela_busca = Table(
            Thead(Tr(Th("Cód"), Th("Data"), Th("Tipo"), Th("Categoria"), Th("Valor"))),
            Tbody(*tabela_busca_linhas)
        ) if tabela_busca_linhas else P("Nenhum lançamento encontrado para a busca realizada.")

        painel_controles_busca = Div(
            Div(
                Form(
                    H4("Pesquisa Sequencial"),
                    Input(type="text", name="busca_seq", placeholder="Digite categoria ou tipo...", value=busca_seq),
                    Input(type="hidden", name="acao", value="buscar"),
                    Button("Buscar Sequencial", type="submit", cls="secondary"),
                    method="post", action="/navegar"
                ),
                style="flex: 1;"
            ),
            Div(
                Form(
                    H4("Pesquisa Binária"),
                    Input(type="number", name="busca_bin", placeholder="Digite o Código (Cód)...", value=busca_bin),
                    Input(type="hidden", name="acao", value="buscar"),
                    Button("Buscar Binaria", type="submit", cls="contrast"),
                    method="post", action="/navegar"
                ),
                style="flex: 1;"
            ),
            cls="grid"
        )

        conteudo = Div(
            H1("Controle Orçamentário Familiar - Buscar"),
            menu_superior,
            painel_controles_busca,
            Hr(),
            H2("Resultados da Busca / Lista de Transações"),
            tabela_busca,
            Hr(),
            A("Voltar ao Início", href="/navegar?acao=cadastrar", role="button", cls="outline"),
            cls="container"
        )
        return Titled("Controle Financeiro - Buscar", conteudo)

    elif acao == "ranking":
        transacoes_ranking = carregar()
        transacoes_ranking = selection_sort(transacoes_ranking, criterio=criterio_ranking)

        tabela_ranking_linhas = [
            Tr(Td(str(t["codigo"])), Td(t["data"]), Td(t["tipo"]), Td(t["categoria"]), Td(f"R$ {t['valor']:.2f}"))
            for t in transacoes_ranking
        ]

        tabela_ranking = Table(
            Thead(Tr(Th("Cód"), Th("Data"), Th("Tipo"), Th("Categoria"), Th("Valor"))),
            Tbody(*tabela_ranking_linhas)
        ) if tabela_ranking_linhas else P("Nenhum lançamento cadastrado para exibição no ranking.")

        controles_ordenacao_ranking = Div(
            H4("Ordenação da Lista de Ranking"),
            Form(
                Input(type="hidden", name="acao", value="ranking"),
                Button("Ordenar por Valor", type="submit", name="criterio_ranking", value="valor", cls="outline"),
                " ",
                Button("Ordenar por Data", type="submit", name="criterio_ranking", value="data", cls="outline"),
                " ",
                Button("Ordenação por Cód", type="submit", name="criterio_ranking", value="codigo", cls="outline"),
                method="post",
                action="/navegar",
                style="display: inline-block;"
            )
        )

        nome_criterio = "Código (Cód)" if criterio_ranking == "codigo" else criterio_ranking.capitalize()

        conteudo = Div(
            H1("Controle Orçamentário Familiar - Ranking e Ordenação"),
            menu_superior,
            controles_ordenacao_ranking,
            Hr(),
            H2(f"Lista de Transações Ordenada por: {nome_criterio}"),
            tabela_ranking,
            Hr(),
            A("Voltar ao Início", href="/navegar?acao=cadastrar", role="button", cls="outline"),
            cls="container"
        )
        return Titled("Controle Financeiro - Ranking", conteudo)

    elif acao == "relatorio":
        transacoes = carregar()

        di_comp = converter_data_para_comparacao(data_inicio)
        df_comp = converter_data_para_comparacao(data_fim)

        transacoes_filtradas = []
        for t in transacoes:
            t_comp = converter_data_para_comparacao(t["data"])
            if t_comp:
                incluir = True
                if di_comp and t_comp < di_comp:
                    incluir = False
                if df_comp and t_comp > df_comp:
                    incluir = False
                if incluir:
                    transacoes_filtradas.append(t)
            elif not di_comp and not df_comp:
                transacoes_filtradas.append(t)

        if not di_comp and not df_comp:
            transacoes_filtradas = transacoes

        transacoes_filtradas = selection_sort(transacoes_filtradas, criterio="data")

        tabela_relatorio_linhas = [
            Tr(Td(str(t["codigo"])), Td(t["data"]), Td(t["tipo"]), Td(t["categoria"]), Td(f"R$ {t['valor']:.2f}"))
            for t in transacoes_filtradas
        ]

        tabela_relatorio = Table(
            Thead(Tr(Th("Cód"), Th("Data"), Th("Tipo"), Th("Categoria"), Th("Valor"))),
            Tbody(*tabela_relatorio_linhas)
        ) if tabela_relatorio_linhas else P("Nenhum lançamento encontrado para o período informado.")

        painel_controles_relatorio = Div(
            Form(
                H4("Filtro de Relatório por Período (De / Até)"),
                Div(
                    Div(
                        Label("Data Inicial (DD/MM/AAAA):", _for="data_inicio"),
                        Input(type="text", name="data_inicio", placeholder="Ex: 01/10/2026", value=data_inicio),
                        cls="grid"
                    ),
                    Div(
                        Label("Data Final (DD/MM/AAAA):", _for="data_fim"),
                        Input(type="text", name="data_fim", placeholder="Ex: 31/10/2026", value=data_fim),
                        cls="grid"
                    ),
                    cls="grid"
                ),
                Input(type="hidden", name="acao", value="relatorio"),
                Button("Filtrar Período", type="submit", cls="secondary"),
                method="post", action="/navegar"
            )
        )

        conteudo = Div(
            H1("Controle Orçamentário Familiar - Relatório"),
            menu_superior,
            painel_controles_relatorio,
            Hr(),
            H2("Lista Completa de Transações Filtradas e Ordenadas por Data (AAAAMMDD)"),
            tabela_relatorio,
            Hr(),
            A("Voltar ao Início", href="/navegar?acao=cadastrar", role="button", cls="outline"),
            cls="container"
        )
        return Titled("Controle Financeiro - Relatório", conteudo)

    return RedirectResponse("/navegar?acao=cadastrar", status_code=303)

@retorno("/adicionar", methods=["POST"])
def post(data: str, tipo: str, categoria: str, valor: float):

    # 1. Validação de data válida
    if not validar_data(data):
        return RedirectResponse("/navegar?acao=cadastrar&erro=data_invalida", status_code=303)

    # 2. Validação de Valor Positivo
    try:
        valor_float = float(valor)
        if valor_float <= 0:
            return RedirectResponse("/navegar?acao=cadastrar&erro=valor_invalido", status_code=303)
    except ValueError:
        return RedirectResponse("/navegar?acao=cadastrar&erro=formato_valor", status_code=303)

    # 3. Validação de Lista Fixa de Domínio
    if tipo not in TIPOS_VALIDOS or categoria not in CATEGORIAS_VALIDAS:
        return RedirectResponse("/navegar?acao=cadastrar&erro=dominio_invalido", status_code=303)

    transacoes = carregar()

    # 4: Regra de validação de Cód
    novo_codigo = 1 if not transacoes else transacoes[-1]["codigo"] + 1
    codigo_existente = any(t["codigo"] == novo_codigo for t in transacoes)
    if codigo_existente:
        novo_codigo = max((t["codigo"] for t in transacoes), default=0) + 1

    # 5: Montagem do dicionário Json
    novo = {
        "codigo": novo_codigo,
        "data": data.strip(),
        "tipo": tipo.strip().lower(),
        "categoria": categoria.strip().lower(),
        "valor": valor_float
    }

    # 6: Persistência no JSON
    transacoes.append(novo)
    salvar(transacoes)

    return RedirectResponse("/navegar?acao=cadastrar", status_code=303)

# ABRIR O BROWSER AUTOMATICAMENTE AO EXECUTAR
if __name__ == "__main__":
    # Abre o navegador padrão na porta 5001 apontando para a rota inicial
    webbrowser.open("http://localhost:5001")
    serve(port=5001)
