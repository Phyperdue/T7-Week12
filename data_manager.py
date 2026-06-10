import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

DB_NAME = "database.db"

def init_database():
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS penjualan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            kategori TEXT,
            produk TEXT,
            jumlah INTEGER,
            harga REAL,
            total REAL
        )
    ''')
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM penjualan")
    if cursor.fetchone()[0] == 0:
        kategori_list = ['Elektronik', 'Fashion', 'Makanan', 'Kesehatan', 'Otomotif']
        produk_map = {
            'Elektronik': ['Smartphone', 'Laptop', 'Earphone', 'Powerbank'],
            'Fashion': ['Kemeja', 'Celana Jeans', 'Jaket', 'Sepatu Sneaker'],
            'Makanan': ['Camilan Box', 'Susu Formula', 'Kopi Premium', 'Roti Gandum'],
            'Kesehatan': ['Vitamin C', 'Masker Medis', 'Suplemen', 'Termometer'],
            'Otomotif': ['Oli Mesin', 'Helm Fullface', 'Sarung Tangan', 'Kaca Spion']
        }
        
        start_date = datetime.now() - timedelta(days=30)
        for i in range(55):
            tgl = (start_date + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            kat = random.choice(kategori_list)
            prod = random.choice(produk_map[kat])
            jml = random.randint(1, 10)
            hrg = random.choice([50000, 120000, 250000, 450000, 750000])
            ttl = jml * hrg
            
            cursor.execute('''
                INSERT INTO penjualan (tanggal, kategori, produk, jumlah, harga, total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (tgl, kat, prod, jml, hrg, ttl))
        conn.commit()
    conn.close()

def get_all_data(kategori_filter=None):
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT * FROM penjualan"
    if kategori_filter and kategori_filter != "Semua Kategori":
        query += f" WHERE kategori = '{kategori_filter}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def insert_data(tanggal, kategori, produk, jumlah, harga):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    total = int(jumlah) * float(harga)
    cursor.execute('''
        INSERT INTO penjualan (tanggal, kategori, produk, jumlah, harga, total)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (tanggal, kategori, produk, jumlah, harga, total))
    conn.commit()
    conn.close()

def delete_data(data_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM penjualan WHERE id = ?", (data_id,))
    conn.commit()
    conn.close()