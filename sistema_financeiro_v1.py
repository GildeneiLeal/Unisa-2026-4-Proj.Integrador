import json
import os
from fasthtml.common import *

# Inicializa o aplicativo FastHTML com Pico CSS habilitado
app, retorno = fast_app(pico=True,
                        hdrs=(Link(rel="stylesheet", href="/static/padrao.css"),),)
ARQUIVO_DADOS = "data/finance_data.json"

def garantir_diretorio_e_arquivo():     # Garante que a pasta 'data' e o arquivo JSON existam.
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

def carregar_registros():    # Lê os dados do arquivo JSON.
    garantir_diretorio_e_arquivo()
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def salvar_registros(registros):    # Salva as registros no arquivo JSON.
    garantir_diretorio_e_arquivo()
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=4)

def selection_sort(registros, criterio="valor"):    # Ordena as registros usando Selection Sort (algoritmo feito à mão).
    n = len(registros)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if criterio == "valor":
                if registros[j]["valor"] < registros[min_idx]["valor"]:
                    min_idx = j
            elif criterio == "data":
                if registros[j]["data"] < registros[min_idx]["data"]:
                    min_idx = j
            elif criterio == "codigo":
                if registros[j]["codigo"] < registros[min_idx]["codigo"]:
                    min_idx = j
        registros[i], registros[min_idx] = registros[min_idx], registros[i]
    return registros

def pesquisa_sequencial(registros, termo):    # Realiza a Pesquisa Sequencial percorrendo a lista.
    if not termo:
        return registros
    termo = termo.lower().strip()
    resultados = []
    for t in registros:
        if (termo in t["categoria"].lower() or
            termo in t["tipo"].lower() or
            termo == str(t["codigo"])):
            resultados.append(t)
    return resultados

def pesquisa_binaria_por_codigo(registros, codigo_alvo):    # Realiza a Pesquisa Binária por código.
    trans_ordenadas = selection_sort(list(registros), criterio="codigo")
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

@retorno("/")
def get(criterio: str = "valor", busca_seq: str = "", busca_bin: str = ""):
    registros = carregar_registros()
    if busca_seq:
        registros = pesquisa_sequencial(registros, busca_seq)
    elif busca_bin:
        try:
            cod_alvo = int(busca_bin)
            registros = pesquisa_binaria_por_codigo(registros, cod_alvo)
        except ValueError:
            registros = []

    if not busca_seq and not busca_bin and criterio in ["valor", "data", "codigo"]:
        registros = selection_sort(registros, criterio)

    total_receitas = sum(t["valor"] for t in registros if t["tipo"] == "receita")
    total_despesas = sum(t["valor"] for t in registros if t["tipo"] == "despesa")
    saldo = total_receitas - total_despesas

    # Painel de Resumo Financeiro posicionado na lateral direita
    painel_resumo = Fieldset(
        Legend("Resumo Financeiro"),
        P(f"Total Receitas: R$ {total_receitas:.2f}"),
        P(f"Total Despesas: R$ {total_despesas:.2f}"),
        P(f"Saldo Atual: R$ {saldo:.2f}"),
    )

    # Formulário de cadastro com rótulos à esquerda
    form_cadastro = Form(
        Fieldset(
            Legend("Novo Lançamento"),
            Div(
                Div(Label("Data (DD/MM/AAAA):", _for="data"), style="flex: 1; min-width: 0;"),
                Div(Input(type="text", id="data", name="data", placeholder="Ex: 25/10/2026", required=True), style="flex: 3; min-width: 250;"),
                style="display: flex; gap: 2rem; align-items: flex-start; width: 100%;"
            ),
            Div(
                Div(Label(" Tipo de Lançamento:", _for="tipo"), style="flex: 1; min-width: 0;"),
                Div(Select(
                        Option("Receita", value="receita"),
                        Option("Despesa", value="despesa"),
                        name="tipo", id="tipo"
                    ), style="flex: 3; min-width: 250;"),
                style="display: flex; gap: 2rem; align-items: flex-start; width: 100%;"
            ),
            Div(
                Div(Label("Categoria:", _for="categoria"), style="flex: 1; min-width: 0;"),
                Div(Select(
                        Option("Salário", value="salario"),
                        Option("Alimentação", value="alimentacao"),
                        Option("Vestuário", value="vestuario"),
                        Option("Saúde", value="saude"),
                        Option("Transporte", value="transporte"),
                        Option("Investimento", value="investimento"),
                        Option("Imposto", value="imposto"),
                        name="categoria", id="categoria", required=True
                    ), style="flex: 3; min-width: 250;"),
                style="display: flex; gap: 2rem; align-items: flex-start; width: 100%;"
            ),
            Div(
                Div(Label("Valor (R$):", _for="valor"), style="flex: 1; min-width: 0;"),
                Div(Input(type="number", step="0.01", id="valor", name="valor", placeholder="0.00", required=True), style="flex: 3; min-width: 250;"),
                style="display: flex; gap: 2rem; align-items: flex-start; width: 100%;"
            ),
            Button("Cadastrar", type="submit", style="width: 200px;")
        ),
        method="post", action="/adicionar"
    )

    # Linhas da tabela de registros
    tabela_linhas = []
    for t in registros:
        tabela_linhas.append(
            Tr(
                Td(str(t["codigo"])),
                Td(t["data"]),
                Td(t["tipo"]),
                Td(t["categoria"]),
                Td(f"R$ {t['valor']:.2f}")
            )
        )

    tabela = Table(
        Thead(Tr(Th("Cód"), Th("Data"), Th("Tipo"), Th("Categoria"), Th("Valor"))),
        Tbody(*tabela_linhas)
    ) if tabela_linhas else P("Nenhum registro encontrado ou cadastrado.")

    # Painel de Controles (Ordenação e Pesquisas)
    painel_controles = Div(
        Div(
            H4("Ordenação"),
            P("Ordenar por Data", href="/?criterio=data", role="button", cls="outline"),
            " ",
            P("Ordenar por Valor", href="/?criterio=valor", role="button", cls="outline"),
            " ",
            P("Ordenar por Cód.", href="/?criterio=codigo", role="button", cls="outline"),
            #style="display: flex; gap: 2rem; align-items: flex-start; width: 100px;"
            style="flex: 1;"
        ),
        Div(
            Form(
                H4("Pesquisa Sequencial"),
                Input(type="text", name="busca_seq", placeholder="Digite categoria ou tipo...", value=busca_seq),
                Button("Buscar (Seq)", type="submit", cls="secondary"),
                method="get", action="/"
            ),
            style="flex: 1;"
        ),
        Div(
            Form(
                H4("Pesquisa Binária"),
                Input(type="number", name="busca_bin", placeholder="Digite o Código (Cód)...", value=busca_bin),
                Button("Buscar (Bin)", type="submit", cls="contrast"),
                method="get", action="/"
            ),
            style="flex: 1;"
        ),
        cls="grid"
    )

    # Organização do Conteúdo Principal com Flexbox inline garantido
    conteudo = Div(
        H1("Controle Orçamentário Familiar"),
        Div(
            Div(form_cadastro, style="flex: 3; min-width: 1;"),
            Div(painel_resumo, style="flex: 1; min-width: 251px; border-style: solid;"),
            style="display: flex; gap: 2rem; align-items: flex-start; width: 100%;"
        ),
        Hr(),
        H2("Lançamentos e Filtros"),
        painel_controles,
        Hr(),
        tabela,
        cls="container"
    )
    return Titled("Controle Financeiro", conteudo)

@retorno("/adicionar", methods=["POST"])
def post(data: str, tipo: str, categoria: str, valor: float):
    registros = carregar_registros()
    novo_codigo = 1 if not registros else registros[-1]["codigo"] + 1

    nova = {
        "codigo": novo_codigo,
        "data": data,
        "tipo": tipo,
        "categoria": categoria,
        "valor": float(valor)
    }

    registros.append(nova)
    salvar_registros(registros)

    return RedirectResponse("/", status_code=303)

serve()
