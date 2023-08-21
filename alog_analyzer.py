#!/usr/bin/env python

import sys
import os
import re
from user_agents import parse as parse_useragent


class Processador:
  _logfile = None
  _logs = []
  
  _log_pattern = r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<bytes>\d+) "-" "(?P<useragent>.*?)"'
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

          self._logs.append(log)
    except:
      Info().app_version()
      print('Houve uma falha no carregamento dos logs')
      Info().usage_brief()
  
  
  def analisar(self):
    
    return None

  def atualizarDB(self):
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
  processador.atualizarDB()
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
