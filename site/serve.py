"""Serve o projeto e reconstrói o site sozinho quando as coleções mudam.

Uso:  python site/serve.py [--port 8000]
Abra http://localhost:8000/site/ e edite à vontade (pastas, planilhas,
animacoes.json, Eixo.txt): o build roda sozinho e a página recarrega.

Sem dependências além do Python.
"""
import functools
import subprocess
import sys
import threading
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "site" / "build.py"
PORT = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8000

built_at = time.time()
pending = False


def snapshot():
    files = [ROOT / "Eixo.txt"]
    for base in [ROOT / "Coleções"]:
        if base.is_dir():
            files += [p for p in base.rglob("*") if p.is_file()]
    return {str(p): p.stat().st_mtime_ns for p in files if p.exists()}


def rebuild():
    global built_at
    print("[serve] mudanças detectadas, rodando build.py ...", flush=True)
    r = subprocess.run([sys.executable, str(BUILD)], capture_output=True, text=True)
    print(r.stdout.strip(), flush=True)
    if r.returncode != 0:
        print(r.stderr.strip(), flush=True)
    else:
        built_at = time.time()


def watcher():
    global pending
    last = snapshot()
    while True:
        time.sleep(2)
        cur = snapshot()
        if cur != last:
            last, pending = cur, True
        if pending:
            pending = False
            time.sleep(1)  # debounce: agrupa saves seguidos
            last = snapshot()
            rebuild()


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/__built":
            body = str(built_at).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()

    def log_message(self, *a):
        pass  # silencioso


if __name__ == "__main__":
    rebuild()  # garante site atualizado ao abrir
    threading.Thread(target=watcher, daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT),
                              functools.partial(Handler, directory=str(ROOT)))
    print(f"[serve] http://localhost:{PORT}/site/  (Ctrl+C para parar)", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
