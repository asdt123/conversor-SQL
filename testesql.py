import sqlite3
import datetime
import pandas as pd
import csv
import re

# Função para tentar converter um valor para int, float ou manter como string
def convert_value(value):
    if isinstance(value, str):
        # Verificar se o valor é um número inteiro
        if re.match(r'^-?\d+$', value):
            return int(value)
        # Verificar se o valor é um número de ponto flutuante
        elif re.match(r'^-?\d+\.\d+$', value):
            return float(value)
    return value

def create_table(start_date, end_date):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS teste''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS teste (
        name VARCHAR(255), 
        identifier INTEGER, 
        wbc DOUBLE PRECISION, 
        lynp DOUBLE PRECISION, 
        midp DOUBLE PRECISION, 
        neup DOUBLE PRECISION, 
        eosp DOUBLE PRECISION,
        monp DOUBLE PRECISION,
        basp DOUBLE PRECISION,
        rbc DOUBLE PRECISION,
        hgb DOUBLE PRECISION, 
        hct DOUBLE PRECISION,
        mcv DOUBLE PRECISION, 
        mch DOUBLE PRECISION, 
        mchc DOUBLE PRECISION,
        rdw_cv DOUBLE PRECISION,
        rdw_sd DOUBLE PRECISION,
        plt DOUBLE PRECISION,
        mpv DOUBLE PRECISION,
        pct DOUBLE PRECISION,
        pdw_cv DOUBLE PRECISION,
        pdw_sd DOUBLE PRECISION,
        plcr DOUBLE PRECISION,
        plcc DOUBLE PRECISION,
        updated_at TIMESTAMP
    )
    ''')

    c.execute('''
    INSERT INTO teste (
        name, identifier, wbc, lynp, midp, neup, eosp, monp, basp, rbc, hgb, hct, mcv, mch, mchc, rdw_cv, rdw_sd, plt, mpv, pct, pdw_cv, pdw_sd, plcr, plcc, updated_at
    ) 
    SELECT name, identifier, wbc,
        CASE WHEN lynp LIKE '%.%' THEN CAST(REPLACE(lynp, ' %', '') AS FLOAT) ELSE lynp END AS lynp,
        CASE WHEN midp LIKE '%.%' THEN CAST(REPLACE(midp, ' %', '') AS FLOAT) ELSE midp END AS midp,
        CASE WHEN neup LIKE '%.%' THEN CAST(REPLACE(neup, ' %', '') AS FLOAT) ELSE neup END AS neup,
        CASE WHEN eosp LIKE '%.%' THEN CAST(REPLACE(eosp, ' %', '') AS FLOAT) ELSE eosp END AS eosp,
        CASE WHEN monp LIKE '%.%' THEN CAST(REPLACE(monp, ' %', '') AS FLOAT) ELSE monp END AS monp,
        CASE WHEN basp LIKE '%.%' THEN CAST(REPLACE(basp, ' %', '') AS FLOAT) ELSE basp END AS basp,
        rbc, hgb, hct, mcv, mch, mchc, rdw_cv, rdw_sd, plt, mpv, pct, pdw_cv, pdw_sd, plcr, plcc, updated_at
    FROM patients
    WHERE updated_at BETWEEN ? AND ? AND NOT name LIKE '%Background%'
''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))


    conn.commit()
    conn.close()

def get_dates():
    while True:
        start_date_str = input("Digite a data inicial (YYYY-MM-DD): ")
        end_date_str = input("Digite a data final (YYYY-MM-DD): ")

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str == '':
                end_date = start_date + datetime.timedelta(days=1)
            else:
                end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')

            if start_date > end_date:
                print("A data inicial não pode ser maior que a data final. Tente novamente.")
            else:
                return start_date, end_date
        except ValueError:
            print("Formato de data inválido. Tente novamente.")

def export_to_csv():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    # Executar uma consulta para selecionar todos os dados da tabela 'teste'
    c.execute('SELECT * FROM teste')
    rows = c.fetchall()
    rows = [";".join(map(str, row)).replace('.', ',',22) for row in rows]
    arquivo_saida =input("insira o nome do arquivo:")
    arquivo_saida+='.csv'
    with open(arquivo_saida, 'w', newline='') as csvfile:
        csvfile.write('name;identifier;wbc;lynp;midp;neup;eosp;monp;basp;rbc;hgb;hct;mcv;mch;mchc;rdw_cv;rdw_sd;plt;mpv;pct;pdw_cv;pdw_sd;plcr;plcc;updated_at\n')
        for row in rows:
            csvfile.write(row + '\n')

    conn.close()

def main():
    start_date, end_date = get_dates()
    create_table(start_date, end_date)
    print("Tabela criada com sucesso.")
    export_to_csv()


if __name__ == "__main__":
    main()
