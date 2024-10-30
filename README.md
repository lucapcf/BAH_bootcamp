# Funções auxiliares Data Fin

Este projeto contém funções utilitárias e dados para o projeto no Google Colab.

## Requisitos

Antes de começar, você precisará ter instalado o Python 3 e o gerenciador de pacotes `pip`.

### Clonando o repositório

```
git clone https://github.com/lucapcf/BAH_bootcamp
```

### Criando um Ambiente Virtual

1. **Navegue até o diretório do seu projeto**:
   ```bash
   cd BAH_bootcamp
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual**

   Windows:
   ```bash
   .venv\Scripts\activate
   ```
   Linux:
   ```bash
   source .venv/bin/activate
   ```

   Após ativar, você verá o nome do ambiente virtual no início do seu prompt de comando.

## Instalando Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias descritas em `requirements.txt` executando:

```bash
pip install -r requirements.txt
```

## Funções

A função identifica os símbolos das ações, remove leituras com NaN e erros no download, e salva em um arquivo os valores válidos.

Execute o seguinte comando:

```python
extract_symbols(filepath: str, exch: str) -> str
check_integrity(filepath: str, start_date: str, end_date: str) -> None
```

- `<filepath.csv>`: caminho do arquivo.
- `<start_date>`: data no formato AAAA-MM-DD.
- `<end_date>`: data no formato AAAA-MM-DD.
- `<exch>`: 'b3', 'nasdaq', 'nyse'.

## Estrutura de Saída

Os scripts vão criar os seguintes arquivos:

- `raw_data/parsed_<nome_do_arquivo>.csv`: Um arquivo CSV com os símbolos extraídos.
- `removed_data/download_failed_parsed_<nome_do_arquivo>.csv`: Um arquivo com os símbolos de ações para os quais os dados não puderam ser baixados.
- `removed_data/NaN_values_parsed_<nome_do_arquivo>.csv`: Um arquivo com os símbolos que contêm valores NaN.
- `pre_processed_data/pre_processed_parsed_<nome_do_arquivo>.csv`: Um arquivo com os símbolos de ações que tiveram dados válidos.

## Desativando o Ambiente Virtual

Quando você terminar de trabalhar, pode desativar o ambiente virtual usando o comando:

```bash
deactivate
```
## Fonte dos Dados

Os dados de ações da NASDAQ podem ser encontrados em: [NASDAQ Stock Screener](https://www.nasdaq.com/market-activity/stocks/screener)
