import sqlite3
import json
# Criar conexão
conn = sqlite3.connect("./workout-fit-file-builder/back/dataBase/fit_files.db")
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS fit_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    binaryData TEXT NOT NULL,
    minutes TEXT, 
    zones TEXT,        
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')


conn.commit()
conn.close()


def save_file_to_db(filename, filepath, minutes, zones):
    with open(filepath, 'rb') as file:
        binary_data = file.read()

    minutes_json = json.dumps(minutes) if isinstance(
        minutes, list) else minutes
    zones_json = json.dumps(zones) if isinstance(zones, list) else zones

    conn = sqlite3.connect(
        "./workout-fit-file-builder/back/dataBase/fit_files.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO fit_files(filename, binaryData,minutes,zones)
    VALUES(?, ?,?,?)''', (filename, binary_data, minutes_json, zones_json))
    conn.commit()
    conn.close()
    return binary_data


def GetFitFile_from_db(filename):
    conn = sqlite3.connect(
        "./workout-fit-file-builder/back/dataBase/fit_files.db")
    cursor = conn.cursor()
    cursor.execute('''
    SELECT binaryData,minutes,zones from fit_files where filename = ?''', (filename,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return (result[0], result[1], result[2])
    else:
        return None


def GetAllNameFiles():
    conn = sqlite3.connect(
        "./workout-fit-file-builder/back/dataBase/fit_files.db")
    cursor = conn.cursor()
    cursor.execute(''' SELECT id,filename from fit_files''')
    rows = cursor.fetchall()
    conn.close
    return rows
