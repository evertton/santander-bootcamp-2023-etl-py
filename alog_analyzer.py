#!/usr/bin/env python

import sys
import os
import re
import pandas
from user_agents import parse as parse_useragent
from pysondb import db as pysondb
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

          log['date'] = datetime.strptime(log['date'], '%d/%b/%Y:%H:%M:%S %z')

          self._logs.append(log)
    except:
      Info.app_version()
      print('Houve uma falha no carregamento dos logs')
      Info.usage_brief()
  
  def _parseDateIndex(self, serie: pandas.core.series.Series, fields: list) -> list:
    date_index = serie.reset_index()
    date_index['year'] = date_index['date'].dt.year
    date_index['month'] = date_index['date'].dt.month
    date_index['day'] = date_index['date'].dt.day

    return date_index[['year', 'month', 'day'] + fields].to_dict(orient='records')

  def analisar(self) -> None:
    logs = pandas.DataFrame(self._logs)
    logs['url'] = logs['request'].apply(lambda x: x['path'])
    
    # Visitas por dia
    #################
    groupedByDateUrl = logs.groupby(['date', 'url'])
    # Visitas únicas
    visitas_unicas_dia = self._parseDateIndex(groupedByDateUrl['ip'].nunique(), ['url', 'ip'])
    # Visitas totais
    visitas_totais_dia = self._parseDateIndex(groupedByDateUrl.size().reset_index(name='hits'), ['url', 'hits'])

    #Database.updateVisitas(visitas_unicas_dia)
    #Database.updateVisitas(visitas_totais_dia)

    # União das visitas únicas e totais
    #visitas_dia = [{**entry1, **entry2} for entry1 in visitas_unicas_dia for entry2 in visitas_totais_dia if (entry1['year'], entry1['month'], entry1['day'], entry1['url']) == (entry2['year'], entry2['month'], entry2['day'], entry2['url'])]

    # Visitas por URL
    #################
    groupedByUrl = logs.groupby(['url'])
    # Visitas únicas
    visitas_unicas_url = groupedByUrl['ip'].nunique()
    # Visitas totais
    visitas_totais_url = groupedByUrl.size()

    print(visitas_unicas_url, visitas_totais_url)

    # Visitas resumo geral
    visitas_unicas_resumo = logs['ip'].nunique()
    visistas_totais_resumo = logs['ip'].count()

    print(visitas_unicas_resumo, visistas_totais_resumo)
  
  def visualizar(self, estatisticas = None):
    if estatisticas is not None:
      pass


class Database:
  _db = pysondb.getDb('alog.db')
  
  @staticmethod
  def updateVisitas(dados:dict = None) -> bool:
    if dados is not None:
      pass
    
    return False


class Info:
  @staticmethod
  def app_version():
    print('Apache Log Analyzer 0.1beta\n---')

  @staticmethod
  def usage_brief():
    print('Uso: alog_analyzer [opções] arquivo\nTente \'alog_analyzer --help\' para mais informações')

  @staticmethod
  def usage():
    usage_msg = '''Uso:
 alog_analyzer [opções] arquivo

Analisa os logs no arquivo de entrada e gera estatísticas

Opções:
 --help        exibe esta ajuda e sai
 --version     exibe a versão
'''
    print (usage_msg)


class ALogAnalyzer:
  def main(log_file):
    processador = Processador(log_file)
    processador.analisar()
    processador.visualizar()
    exit(0)


if __name__ == "__main__":
  command = '--help'

  if len(sys.argv) > 1:
    command = sys.argv[1]

  match command:
    case '--version':
      Info.app_version()
    case '--help':
      Info.app_version()
      Info.usage()
    case _:
      if sys.argv[1][0] == sys.argv[1][1] == '-':  
        Info.app_version()
        print('Opção desconhecida', sys.argv[1])
        Info.usage_brief()
      else:
        if not (os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1])):
          Info.app_version()
          print('Não foi localizado um arquivo no caminho:', sys.argv[1])
          Info.usage_brief()
        else:
          ALogAnalyzer.main(sys.argv[1])
