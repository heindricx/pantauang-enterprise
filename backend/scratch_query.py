import pymysql
import json
import urllib.parse

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
            
            data = []
            for row in result:
                data.append({
                    "Provinsi": row[0] or "Tidak Diketahui",
                    "Ekstrem": int(row[1]),
                    "Tinggi": int(row[2]),
                    "Menengah": int(row[3]),
                    "Rendah": int(row[4]),
                    "Total": int(row[5])
                })
                
            print(json.dumps(data, indent=2))
    finally:
        conn.close()

if __name__ == "__main__":
    run_query()
