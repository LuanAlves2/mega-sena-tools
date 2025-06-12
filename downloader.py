import os
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import unidecode
import re

def download_and_process(
    url: str = "https://asloterias.com.br/download-todos-resultados-mega-sena"
) -> str:
    os.makedirs("database", exist_ok=True)
    logging.info(f"Acessando página de download: {url}")
    session = requests.Session()
    resp = session.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Localiza e submete o form adequado
    form = None
    for fname in ['frm46s', 'frm48s']:
        form = soup.find('form', attrs={'name': fname}) or soup.find('form', attrs={'id': fname})
        if form:
            logging.info(f"Formulário '{fname}' encontrado para download.")
            break
    if form:
        action = form.get('action') or url
        post_url = requests.compat.urljoin(url, action)
        data = {inp.get('name'): inp.get('value', '') for inp in form.find_all('input') if inp.get('name')}
        logging.info(f"Enviando POST para {post_url} com campos: {list(data.keys())}")
        rfile = session.post(post_url, data=data)
    else:
        a = soup.find('a', attrs={'title': re.compile(r'Mega Sena.*Excel', re.I)})
        if a and a.get('href'):
            href = a['href']
            if href.startswith('javascript:'):
                m = re.search(r'document\.(\w+)\.submit', href)
                if m:
                    fname = m.group(1)
                    form = soup.find('form', attrs={'name': fname}) or soup.find('form', attrs={'id': fname})
                    action = form.get('action') or url
                    post_url = requests.compat.urljoin(url, action)
                    data = {inp.get('name'): inp.get('value', '') for inp in form.find_all('input') if inp.get('name')}
                    logging.info(f"Enviando POST para {post_url} com campos: {list(data.keys())}")
                    rfile = session.post(post_url, data=data)
                else:
                    logging.info("JS genérico detectado, POST vazio para URL principal")
                    rfile = session.post(url)
            else:
                dl_url = requests.compat.urljoin(url, href)
                logging.info(f"Baixando diretamente de: {dl_url}")
                rfile = session.get(dl_url)
        else:
            raise RuntimeError("Não foi possível encontrar form ou link de download Excel.")

    rfile.raise_for_status()
    ctype = rfile.headers.get('Content-Type', '')
    logging.info(f"Content-Type retornado: {ctype}")

    if 'spreadsheetml' not in ctype and 'ms-excel' not in ctype:
        alt_name = f"database/mega_sena_raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(alt_name, 'wb') as f: f.write(rfile.content)
        logging.error(f"Arquivo não é Excel ({ctype}). Salvado em {alt_name}")
        print(f"Erro: provável HTML salvo em {alt_name}.")
        return alt_name

    raw_filename = f"database/mega_sena_raw_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    with open(raw_filename, 'wb') as f: f.write(rfile.content)
    logging.info(f"Excel bruto salvo como {raw_filename}")

    df = pd.read_excel(raw_filename, engine='openpyxl', skiprows=6)

    col_map = {}
    for col in df.columns:
        cn = unidecode.unidecode(str(col)).strip().lower()
        if re.search(r'concurso|nr\.?\s?sorteio', cn):
            col_map[col] = 'concurso'
        elif 'data' in cn:
            col_map[col] = 'data'
        else:
            m = re.search(r'dezena.*?(\d+)', cn) or re.search(r'bola\s*(\d+)', cn)
            if m:
                col_map[col] = f"dezena{m.group(1)}"
    df = df.rename(columns=col_map)

    dez_cols = sorted([c for c in df.columns if c.startswith('dezena')], key=lambda x: int(x.replace('dezena','')))
    cols = ['concurso','data'] + dez_cols
    df = df.loc[:, [c for c in cols if c in df.columns]]

    df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')

    try:
        os.remove(raw_filename)
        logging.info(f"Arquivo bruto {raw_filename} removido.")
    except OSError:
        pass

    out_name = "database/mega_sena_sorteios_passados.xlsx"
    df.to_excel(out_name, index=False)
    logging.info(f"Arquivo processado salvo como {out_name}")
    print(f"Download e processamento concluídos: {out_name}")

    return out_name 