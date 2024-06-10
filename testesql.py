import sqlite3
import datetime
import csv

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
    SELECT name, identifier, wbc, lynp, midp, neup, eosp, monp, basp, rbc, hgb, hct, mcv, mch, mchc, rdw_cv, rdw_sd, plt, mpv, pct, pdw_cv, pdw_sd, plcr, plcc, updated_at FROM patients WHERE updated_at BETWEEN ? AND ? and not name LIKE '%Background%'   ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))

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
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    c.execute('SELECT * FROM teste')
    rows = c.fetchall()
    arquivo_saida =input("insira o nome do arquivo:")
    arquivo_saida+='.csv'
    with open(arquivo_saida, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['name', 'identifier', 'wbc', 'lynp', 'midp', 'neup', 'neup', 'eosp', 'monp', 'rbc', 'hgb', 'hct', 'mcv', 'mch', 'mchc', 'rdw_cv', 'rdw_sd', 'plt', 'mpv', 'pct', 'pdw_cv', 'pdw_sd', 'plcr', 'plcc', 'updated_at'])
        csvwriter.writerows(rows)

    conn.close()

def main():
    start_date, end_date = get_dates()
    create_table(start_date, end_date)
    print("Tabela criada com sucesso.")
    export_to_csv()


if __name__ == "__main__":
    main()
