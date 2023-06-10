import sqlite3

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, nome text, estrelas real, diaria real, cidade text)"
cria_usuario = "CREATE TABLE IF NOT EXISTS usuarios (user_id int PRIMARY KEY, login text, senha text"

cria_hotel = "INSERT INTO hoteis VALUES('alpha', 'Alpha Hotel', 4.3, 319.99, 'Sao Paulo')"

cursor.execute(cria_tabela)

conexao.commit()
conexao.close()
