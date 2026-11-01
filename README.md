# Unisa-2026-4-Proj.Integrador

## 🚀 Notas de Atualização — Release `v0.2.0-beta_02`

[![FastHTML](https://img.shields.io/badge/FastHTML-Framework-blue)](https://fastht.ml/)
[![Pico CSS](https://img.shields.io/badge/UI-Pico%20CSS-108575)](https://picocss.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](https://www.python.org/)

Esta versão marca a migração do sistema **Controle Orçamentário Familiar** de uma visão única (monopágina) para uma **arquitetura de visões independentes e isoladas por rotas de navegação** (`/navegar`), aprimorando a experiência do usuário e a organização algorítmica dos módulos.

---

### 📋 Comparativo: `sistema_financeiro_v1.py` ➔ `sistema_financeiro_v2.py` (`beta_02`)

| Funcionalidade / Aspecto | Arquivo `sistema_financeiro_v1.py` (v0.1) | Arquivo `sistema_financeiro_v2.py` (v0.2-beta_02) |
| :--- | :--- | :--- |
| **Arquitetura de Navegação** | Monopágina (formulário, buscas e ordenação no mesmo fluxo) | **Menu Superior dinâmico** com telas isoladas (`Cadastrar`, `Listar`, `Buscar`, `Ranking`, `Relatório`) |
| **Tratamento de Ordenação** | Ordenação simples (com erro de prioridade em strings de data) | **Selection Sort aprimorado**: conversão automática de `DD/MM/AAAA` para `AAAAMMDD` |
| **Módulo de Busca** | Painel de busca acoplado na tela principal | **Tela "Buscar" exclusiva**: Pesquisa Sequencial e Pesquisa Binária (por Código) isoladas com réplica da tabela |
| **Módulo de Ranking** | Botões simples na página inicial | **Tela "Ranking" dedicada**: suporte aos critérios *Valor*, *Data* e novo botão exclusivo *Ordenação por Cód.* |
| **Módulo de Relatórios** | Não implementado | **Tela "Relatório" exclusiva**: filtro por período (`De` / `Até`) com ordenação cronológica automática (`AAAAMMDD`) |
| **Estilização e Layout (CSS)** | CSS Inline básico (`style="..."`) | **CSS Customizado (`padrao.css`)**: rótulos e campos lado a lado (`.campo-horizontal`), painel flexível sem altura fixa |

---

### ✨ Novas Features & Implementações

#### 1. 🔘 Menu Superior Dinâmico e Rotas Centralizadas
- Implementação da função centralizadora `@retorno("/navegar")` para tratar requisições HTTP `POST`/`GET`.
- Cada botão do menu agora carrega um módulo isolado com seu próprio título e conjunto de controles sem poluição visual.

#### 2. 📅 Ordenação Cronológica Precisa (`AAAAMMDD`)
- Ajuste no algoritmo **Selection Sort** para decompor datas brasileiras (`DD/MM/AAAA`) no formato normalizado `AAAAMMDD` antes de efetuar comparações textuais, corrigindo a ordenação cronológica em todas as telas.

#### 3. 🔍 Módulo de Busca Isolado
- Transferência da **Pesquisa Sequencial** (por categoria/tipo) e **Pesquisa Binária** (por código) para a tela `Buscar`, exibindo apenas os resultados correspondentes na tabela filtrada.

#### 4. 📊 Módulo de Relatório por Período (De / Até)
- Novo painel de filtragem por intervalo de datas iniciais e finais na aba `Relatório`, ordenando automaticamente os resultados por data.

#### 5. 🎨 Design & Ajustes de Layout (`padrao.css`)
- **Alinhamento Lado a Lado (`.campo-horizontal`)**: Rótulos e inputs/selects alinhados na mesma linha com largura proporcional.
- **Correção de Altura Fixo**: Remoção de limitações (`height: 960px`) para evitar grandes lacunas em branco entre o formulário e a tabela de lançamentos.

---

### 💻 Como Executar a Versão `beta_02`

```bash
# Clone o repositório
git clone [https://github.com/GildeneiLeal/seu-repositorio.git](https://github.com/GildeneiLeal/seu-repositorio.git)

# Acesse a pasta do projeto
cd Sistema

# Execute a versão atualizada
python sistema_financeiro_v2.py
