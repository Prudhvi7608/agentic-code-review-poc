def fetch_icd_data(cursor):
    query = "SELECT * FROM icd_codes"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def process_icd(icd_list):
    for code in icd_list:
        print(f"Processing code: {code}")
