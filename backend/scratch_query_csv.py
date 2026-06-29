import pymysql
import csv
import os

def run_query():
    host = "gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com"
    port = 4000
    user = "KnokxJmGN7Viird.root"
    password = "O3GrrtV167xYXanO"
    db_name = "test"
    
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )
    
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT 
                provinsi,
                SUM(CASE WHEN skor_risiko >= 90.16 THEN 1 ELSE 0 END) as ekstrem,
                SUM(CASE WHEN skor_risiko >= 23.75 AND skor_risiko < 90.16 THEN 1 ELSE 0 END) as tinggi,
                SUM(CASE WHEN skor_risiko > 0 AND skor_risiko < 23.75 THEN 1 ELSE 0 END) as menengah,
                SUM(CASE WHEN skor_risiko = 0 THEN 1 ELSE 0 END) as rendah,
                COUNT(*) as total
            FROM procurement_anomalies
            GROUP BY provinsi
            ORDER BY ekstrem DESC, tinggi DESC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            output_path = r"D:\satdat 2026\sec\pantauang-enterprise\rekap_risiko_provinsi.csv"
            
            with open(output_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Provinsi", "Anomali Ekstrem", "Risiko Tinggi", "Risiko Menengah", "Risiko Rendah", "Total Paket"])
                
                for row in result:
                    writer.writerow([
                        row[0] or "Tidak Diketahui",
                        int(row[1]),
                        int(row[2]),
                        int(row[3]),
                        int(row[4]),
                        int(row[5])
                    ])
                    
            print(f"File CSV berhasil dibuat: {output_path}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_query()
