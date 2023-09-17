# Apache Log Analyzer

Aqui estão as etapas típicas que você pode seguir para realizar o processo de ETL em arquivos de log do Apache usando Python:

1. Extração:
    - Abra o arquivo de log do Apache usando Python.
    - Leia as linhas do arquivo de log e extraia as informações relevantes, como endereço IP, data/hora, método HTTP, URL, código de status, tamanho da resposta, etc.

2. Transformação:
    - Realize as transformações necessárias nos dados extraídos. Isso pode incluir a limpeza de dados, a conversão de formatos, a agregação de informações, a filtragem de registros, etc. Por exemplo, você pode calcular estatísticas, agrupar registros por hora/dia/mês, ou converter formatos de data/hora.

3. Carregamento:
    - Carregue os dados transformados em um local de armazenamento de sua escolha. Isso pode ser um banco de dados relacional (como MySQL, PostgreSQL), um banco de dados NoSQL (como MongoDB), ou um arquivo de saída (como CSV ou JSON).

## Uso
```
 alog_analyzer [opções] arquivo
```
Analisa os logs no arquivo de entrada e gera estatísticas

### Argumentos:
 `arquivo`             caminho para o arquivo de log

### Opções:
```
 -h, --ajuda         exibe esta ajuda e sai
 -v, --ver           exibe os dados após o processamento
 -l, --limpar        limpa o banco de dados
 -a, --adicionar     insere os novos valores no banco de dados mantendo os existentes
 -s, --substituir    limpa o banco de dados, após insere novos valores (comportamento padrão)
 --versao            exibe a versão
```

 ## Gerando 