#!/usr/bin/env python

import random
import datetime

# Lista de IPs fictícios
ips = [f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}" for _ in range(50)]

# Lista de métodos HTTP e códigos de status
http_methods = ["GET", "POST", "PUT", "DELETE"]
http_status_codes = [200, 201, 204, 400, 404, 500]

# Lista de URLs fictícias
urls = ["/page1", "/page2", "/page3", "/api/resource1", "/api/resource2"]

# Lista de user agents fictícios
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/93.0.961.38 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.31 Safari/537.36 Edg/94.0.992.18",
]

# Gerar as linhas de logs
for _ in range(10):
    # Gerar um IP fictício
    ip = random.choice(ips)

    # Gerar uma data e hora fictícia entre janeiro e agosto de 2023
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2023, 8, 31)
    current_time = (start_date + (end_date - start_date) * random.random()).strftime("%d/%b/%Y:%H:%M:%S %z")

    # Escolher aleatoriamente os componentes do log
    method = random.choice(http_methods)
    url = random.choice(urls)
    status_code = random.choice(http_status_codes)
    size_bytes = random.randint(200,1024)
    user_agent = random.choice(user_agents)

    # Montar a linha de log
    log_line = f'{ip} - - [{current_time}+0000] "{method} {url} HTTP/1.1" {status_code} {size_bytes} "-" "{user_agent}"'
    print(log_line)
