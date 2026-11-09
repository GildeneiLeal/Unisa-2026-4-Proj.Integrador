# 📊 Sistema Web Modular para Controle Orçamentário Familiar

[![FastHTML](https://img.shields.io/badge/FastHTML-Framework-blue)](https://fastht.ml/)
[![Pico CSS](https://img.shields.io/badge/UI-Pico%20CSS-108575)](https://picocss.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Release-v0.2.0--beta__02-green)](#)

## 📝 Resumo do Projeto
Este projeto consiste no desenvolvimento de uma aplicação web voltada ao controle orçamentário familiar, integrando o framework **FastHTML**, estilização com **Pico CSS** e rotinas algorítmicas puras de busca e ordenação customizadas em **Python**. 

O sistema foi concebido como uma **evolução natural** do modelo monolítico de terminal (linha de comando / CSV) proposto nas aulas do **Laboratório de Programação (UNISA)**, migrando para uma **arquitetura web baseada em rotas de navegação independentes (`/navegar`) e persistência segura em formato JSON**.

---

## 🔍 Comparativo Técnico: `main_3.py` (v0.1) vs `sistema_financeiro_vBeta.py` (`beta_02`)

| Funcionalidade / Aspecto | Protótipo Inicial (`main_3.py`) | Versão Atual (`sistema_financeiro_vBeta.py`) | Evolução e Impacto Prático |
| :--- | :--- | :--- | :--- |
| **Arquitetura de Navegação** | Monopágina (`GET /` concentrando formulários, buscas e listagem) | **Arquitetura de Visões Isoladas** via rota centralizadora `@retorno("/navegar")` | Elimina a sobrecarga cognitiva e organiza as responsabilidades em abas dedicadas: *Cadastrar*, *Listar*, *Buscar*, *Ranking* e *Relatório*. |
| **Validação de Negócio** | Apensas restrições básicas do HTML (`required`) | **Backend Validador Restrito**: validação manual de datas, valor estritamente positivo e checagem de domínio fixo | Garante integridade absoluta no arquivo JSON, prevenindo registros corrompidos e datas inexistentes (ex: `31/02`). |
| **Validação Cronológica (Datas)** | Comparação textual direta de strings `DD/MM/AAAA` | **Algoritmo de Normalização de Chave (`AAAAMMDD`)** integrado ao *Selection Sort* | Elimina falhas de ordenação textual onde "01/12/2025" era considerado menor que "02/01/2026". |
| **Pesquisa e Consulta** | Painel de busca acoplado e fixo na página inicial | **Aba "Buscar" Exclusiva**: alternância entre *Pesquisa Sequencial* (por tipo/categoria) e *Pesquisa Binária* (por código único) | Permite consultar lançamentos de forma isolada sem poluição visual. |
| **Módulo de Relatórios** | Não implementado | **Tela "Relatório" com filtro por período (`De` / `Até`)** | Filtra e reordena os dados dinamicamente no padrão de comparação cronológica `AAAAMMDD`. |
| **Execução e usabilidade** | Execução manual em terminal (`python main_3.py`) | **Execução Automatizada**: inicialização com `webbrowser.open()` e suporte a empacotamento standalone (`.exe`) | O usuário executa com um duplo clique e o navegador abre automaticamente apontando para `http://localhost:5001`. |

---

### 🛡️ Regras de Validação e Integridade dos Dados

A versão `sistema_financeiro_vBeta.py` implementa validações defensivas no backend antes de persistir os dados no arquivo `data/finance_data.json`:
1. **Validação de Data Manual (`validar_data`)**: Função puramente lógica (sem dependências externas) que analisa o formato `DD/MM/AAAA`, valida os dias máximos de cada mês e calcula anos bissextos (rejeitando entradas inválidas como `31/02`).
2. **Valor Estritamente Positivo**: Rejeita valores nulos ou negativos (`valor <= 0`), enviando um alerta visual (`?erro=valor_invalido`) em destaque avermelhado na interface.
3. **Domínio Fixo de Categorias e Tipos**: Valida entradas contra as constantes globais `CATEGORIAS_VALIDAS` e `TIPOS_VALIDOS`.
4. **Garantia de Código Único**: Recalcula e valida o identificador único da transação, prevenindo colisões ou duplicidades.

---

### 💻 Como Executar a Aplicação

#### Instalando e configurando o Pyhton
1. Baixe e instale o Python em seu sistema operacional
https://python.org.br/instalacao-windows/

2. Forçar a instalação e ativação do pip pelo Python
Execute o comando abaixo para garantir que o gerenciador de pacotes seja instalado/atualizado corretamente na sua versão do Python:

python -m ensurepip --upgrade

3. Atualizar o pip para a versão mais recente

python -m pip install --upgrade pip

4. Instalar o FastHTML corretamente
O nome oficial do pacote do FastHTML no registrador do Python é python-fasthtml. Instale-o utilizando o próprio Python para evitar erros de caminho:

python -m pip install python-fasthtml

5. Executar o seu sistema financeiro novamente
Agora que o módulo foi instalado com sucesso no ambiente correto, rode o seu script:

python sistema_financeiro_vBeta.py


#### Opção 1: Direto via Python
```bash
# Clone o repositório
git clone https://github.com/GildeneiLeal/Unisa-2026-4-Proj.Integrador.git

# Acesse a pasta do projeto
cd Unisa-2026-4-Proj.Integrador

# Execute o arquivo da versão atual
python sistema_financeiro_vBeta.py
```
*O sistema iniciará o servidor local e abrirá automaticamente o seu navegador em `http://localhost:5001`.*

#### Opção 2: Gerar o Executável Standalone (`.exe`)
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole sistema_financeiro_vBeta.py
```
*O arquivo executável será gerado na pasta `dist/` e poderá ser executado com um duplo clique sem necessidade de ter o Python instalado.*

---

## 📚 Referências Normativas e Bibliográficas (Padrão ABNT NBR 14724)

ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **ABNT NBR 14724**: informação e documentação: trabalhos acadêmicos: apresentação. Rio de Janeiro: ABNT, 2011.

CORMEN, Thomas H. et al. **Algoritmos: Teoria e Prática**. 3. ed. Rio de Janeiro: Elsevier, 2012.

GEMINI AI. **Auxílio do Gemini AI para Desenvolvimento de Código**. Google AI, 2026. Disponível em: <https://gemini.google.com/>. Acesso em: 03 nov. 2026.

NIELSEN, Jakob. **Projetando Websites com Usabilidade**. Rio de Janeiro: Campus, 2000.

RAMALHO, Luciano. **Python Fluente: Programação Clara, Concisa e Eficaz**. 2. ed. São Paulo: Novatec, 2023.

SAID, S. A. **Finanças Pessoais: Um estudo de caso sobre a importância do orçamento familiar**. Revista de Administração e Contabilidade, v. 14, n. 2, p. 45-58, 2021.

UNISA. **Projeto Integrador: Laboratório de Programação**. São Paulo: Universidade Santo Amaro, 2026.
