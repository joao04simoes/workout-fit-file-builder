import sqlite3

# Criar conexão
conn = sqlite3.connect("./dataBase/fit_files.db")
cursor = conn.cursor()

# Criar tabela para armazenar metadados e caminhos dos ficheiros

cursor.execute('''
CREATE TABLE IF NOT EXISTS fit_files(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')


conn.commit()
conn.close()


def save_file_to_db(filename, filepath):
    with open(filepath, 'rb') as file:
        binary_data = file.read()

    conn = sqlite3.connect("./dataBase/fit_files.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO fit_files(filename, filepath)
    VALUES(?, ?)''', (filename, binary_data))
    conn.commit()
    conn.close()
