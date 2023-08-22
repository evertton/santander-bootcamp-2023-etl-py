#!/usr/bin/env python

import sys
import os
import re
import pandas as pd
from user_agents import parse as parse_useragent
from pysondb import db
from datetime import datetime


class Processador:
  _logfile = None
  _logs = []
  
  _log_pattern = r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<bytes>\d+) "-" "(?P<useragent>.*?)"'
  _request_pattern = r'(?P<method>.*?) (?P<path>.*?) (?P<protocol>.*?)\/(?P<version>[\d|.]+)'
  
  def __init__(self, logfile = None):
    if logfile is not None:
      self.carregar(logfile)

  def carregar(self, logfile):
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
      Info().app_version()
      print('Houve uma falha no carregamento dos logs')
      Info().usage_brief()
  
  
  def analisar(self):
    logs = pd.DataFrame(self._logs)
    logs['url'] = logs['request'].apply(lambda x: x['path'])
    
    groupedByUrlDate = logs.groupby(['url', 'date'])
    visitas_unicas_dia = groupedByUrlDate['ip'].nunique()
    visitas_totais_dia = groupedByUrlDate.size()

    # print(visitas_unicas_dia, visitas_totais_dia)

    groupedByUrl = logs.groupby(['url'])
    visitas_unicas_url = groupedByUrl['ip'].nunique()
    visitas_totais_url = groupedByUrl.size()

    # print(visitas_unicas_url, visitas_totais_url)

    visitas_unicas_resumo = logs['ip'].nunique()
    visistas_totais_resumo = logs['ip'].count()

    # print(visitas_unicas_resumo, visistas_totais_resumo)

    _db = db.getDb('alog.json')
    _db.deleteAll()
    #_db.addMany(visitas_unicas)

  def atualizar_estatisticas(self):
    return None
  
  def visualizar(self):
    return None


class Info:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(Info, cls).__new__(cls)
    return cls._instance

  def app_version(self):
    print('Apache Log Analyzer 0.1beta\n---')

  def usage_brief(self):
    print('Uso: alog_analyzer [opções] arquivo\nTente \'alog_analyzer --help\' para mais informações')

  def usage(self):
    usage_msg = '''Uso:
 alog_analyzer [opções] arquivo

Analisa os logs no arquivo de entrada e gera estatísticas

Opções:
 --help        exibe esta ajuda e sai
 --version     exibe a versão
'''
    print (usage_msg)


def main(log_file):
  processador = Processador(log_file)

  processador.analisar()
  processador.atualizar_estatisticas()
  processador.visualizar()

  exit(0)


if __name__ == "__main__":
  command = '--help'

  if len(sys.argv) > 1:
    command = sys.argv[1]

  match command:
    case '--version':
      Info().app_version()
    case '--help':
      Info().app_version()
      Info().usage()
    case _:
      if sys.argv[1][0] == sys.argv[1][1] == '-':  
        Info().app_version()
        print('Opção desconhecida', sys.argv[1])
        Info().usage_brief()
      else:
        if not (os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1])):
          Info().app_version()
          print('Não foi localizado um arquivo no caminho:', sys.argv[1])
          Info().usage_brief()
        else:
          main(sys.argv[1])
