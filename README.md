# 🛠️ Conversor de Logs - ETL de Arquivos `.log` para `.csv`

Este projeto é um **conversor automatizado de arquivos de log** para formato `.csv`, com funcionalidades de ordenação e extração de informações úteis. Foi desenvolvido com o objetivo de facilitar a análise de dados de conexão, especialmente testes de ping, em que o tempo de resposta ou a perda de pacotes são monitorados.

---

## 📄 Descrição do Projeto

Todos os arquivos `.log` utilizados neste projeto seguem o **mesmo padrão de estrutura**, onde cada log contém:
- **Data** da execução
- **Horário** de cada ping
- Valor do **ping** (ou `2000` caso tenha ocorrido uma perda)
- Indicação de **sucesso ou falha** do ping

---

## 🚀 Etapas do Processo

1. **Extração e Transformação dos Logs**
   - Os arquivos `.log` de uma pasta são lidos.
   - Cada linha relevante é processada para extrair as informações úteis.
   - Os dados são gravados em um arquivo CSV chamado `log.csv`.

2. **Ordenação dos Dados**
   - O arquivo CSV é carregado em um DataFrame.
   - Os dados são ordenados por **data e horário**.
   - Um novo arquivo `log-ordenado.csv` é gerado com os dados organizados.

3. **Coleta de Informações Úteis**
   - Contagem de pings com **sucesso** e **erro** (ping == 2000).
   - Cálculo da **média dos pings com sucesso**.
   - Os resultados são salvos no arquivo `informacoes_uteis.csv`.

> ⚠️ Os pings com erro (`2000`) **não são considerados** na média para evitar distorções.

---

## 📁 Estrutura Esperada dos Arquivos `.log`

- Segunda linha contém a **data**
- A partir da terceira linha:
  - **Horário do ping**
  - Se contiver `"error"`, significa que houve perda
  - Caso contrário, o valor do ping está nos últimos 3 dígitos

---

## 🧠 Tecnologias Utilizadas

- Python 3
- Pandas
- CSV (módulo nativo)
- glob / os / datetime

