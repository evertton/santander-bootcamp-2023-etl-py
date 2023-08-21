#!/usr/bin/env python

import sys
import os


class Processador:
  _instance = None
  _logfile = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(Processador, cls).__new__(cls)
    return cls._instance
  
  def carregar(self, file):
    # ...
    return self.transformar()
  
  def transformar(self):
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
  processador = Processador()

  if not processador.carregar(log_file):
    Info().app_version()
    print('Houve uma falha no carregamento dos logs')
    Info().usage_brief()
    exit(0)

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
