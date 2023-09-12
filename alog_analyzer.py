#!/usr/bin/env python

import sys
import os
import re
import pandas
from sqlalchemy import create_engine, Table, MetaData
from user_agents import parse as parse_useragent
from datetime import datetime


class Processador:
  _logfile = None
  _logs = []
  _estatisticas = []
  
  _log_pattern = r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<bytes>\d+) "-" "(?P<useragent>.*?)"'
  _request_pattern = r'(?P<method>.*?) (?P<path>.*?) (?P<protocol>.*?)\/(?P<version>[\d|.]+)'
  
  def __init__(self, logfile:str = None):
    if logfile is not None:
      self.carregar(logfile)

  def carregar(self, logfile:str) -> None:
    try:
      self._logfile = open(logfile, 'r')

      for line in self._logfile:
        match_log = re.match(self._log_pattern, line)
        if match_log:
          log = match_log.groupdict()

          match_request = re.match(self._request_pattern, log['request'])
          if match_request:
            log['request'] = match_request.groupdict()
          
          useragent = parse_useragent(log['useragent'])
          log['useragent'] = {'browser': useragent.browser.family, 'platform': useragent.os.family}

          log['date'] = datetime.strptime(log['date'], '%d/%b/%Y:%H:%M:%S %z').date()

          self._logs.append(log)
    except:
      Info.app_version()
      print('Houve uma falha no carregamento dos logs')
      Info.usage_brief()
  
  def analisar(self) -> None:
    logs = pandas.DataFrame(self._logs)
    logs['url'] = logs['request'].apply(lambda x: x['path'])
    
    # Visitas por dia
    #################
    groupedByDateUrl = logs.groupby(['date', 'url'])
    # Visitas únicas
    visitas_dia = groupedByDateUrl['ip'].nunique().reset_index()[['date','url','ip']]
    # Visitas totais
    visitas_dia['hits'] = groupedByDateUrl.size().reset_index(name='hits')['hits']
    
    Database.save(Database.TABLE_VISITAS_DIA, visitas_dia)

    # Visitas por URL
    #################
    groupedByUrl = logs.rename(columns={'url': 'url2'}).groupby('url2')
    # Visitas únicas
    visitas_url = groupedByUrl['ip'].nunique().reset_index(name='ip')
    # Visitas totais
    visitas_url['hits'] = groupedByUrl.size().reset_index(name='hits')['hits']

    Database.save(Database.TABLE_VISITAS_URL, visitas_url)
  
  def visualizar(self, estatisticas = None):
    if estatisticas is not None:
      pass


class Database:
  TABLE_VISITAS_DIA = 'visitas_dia'
  TABLE_VISITAS_URL = 'visitas_url'

  _if_exists = 'replace'
  _engine = create_engine('sqlite:///alog.db')
  
  @staticmethod
  def destroy() -> None:
    Table(Database.TABLE_VISITAS_DIA, MetaData()).drop(Database._engine, checkfirst=True)
    Table(Database.TABLE_VISITAS_URL, MetaData()).drop(Database._engine, checkfirst=True)

  @staticmethod
  def save(table:str, dados:pandas.core.frame.DataFrame = None) -> bool:
    if dados is not None:
      dados.to_sql(table, con=Database._engine, if_exists=Database._if_exists, index_label='index')
      return True
    
    return False


class Info:
  @staticmethod
  def app_version():
    print('Apache Log Analyzer 0.1beta\n---')

  @staticmethod
  def usage_brief():
    print('Uso: alog_analyzer [opções] arquivo\nTente \'alog_analyzer --ajuda\' para mais informações')

  @staticmethod
  def usage():
    usage_msg = '''Uso:
 alog_analyzer [opções] arquivo

Analisa os logs no arquivo de entrada e gera estatísticas

Argumentos:
 arquivo             caminho para o arquivo de log

Opções:
 -h, --ajuda         exibe esta ajuda e sai
 -v, --ver           exibe os dados após o processamento
 -l, --limpar        limpa o banco de dados
 -a, --adicionar     insere os novos valores no banco de dados mantendo os existentes
 -s, --substituir    limpa o banco de dados, após insere novos valores (comportamento padrão)
 --versao            exibe a versão
'''
    print (usage_msg)


class ALogAnalyzer:

  def processar(logfile):
    processador = Processador(logfile)
    processador.analisar()

  def visualizar():
    pass

  def main():
    command = "--ajuda"

    if len(sys.argv) > 1:
      command = sys.argv[1]

    match command:
      case "--versao":
        Info.app_version()
      case "-h" | "--ajuda":
        Info.app_version()
        Info.usage()
      case "-l" | "--limpar":
        Database.destroy()
        Info.app_version()
        print("Banco de dados limpos...")
      case _:
        logfile = sys.argv[1]
        if sys.argv[1][0] == "-":
          if command == "-a" or command == "--adicionar":
            Database._if_exists = "append"
            sys.argv[1] = sys.argv[2]
          elif command == "-v" or command == "--ver":
            ALogAnalyzer._view = True
            if not len(sys.argv) > 2:
              ALogAnalyzer.visualizar()
              exit(0)
            
            logfile = sys.argv[2]
          else:
            Info.app_version()
            print("Opção desconhecida", sys.argv[1])
            Info.usage_brief()
            exit(0)
        
        if not (os.path.exists(logfile) and os.path.isfile(logfile)):
          Info.app_version()
          print("Não foi localizado um arquivo no caminho:", logfile)
          Info.usage_brief()
        else:
          ALogAnalyzer.processar(logfile)

if __name__ == "__main__":
  ALogAnalyzer.main()
