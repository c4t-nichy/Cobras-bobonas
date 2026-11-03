import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from crypto_utils import decrypt_text, encrypt_text


PAGE = Path(__file__).parent / "templates" / "index.html"
MAX_BODY_SIZE = 1_000_000


class TextCipherHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if urlsplit(self.path).path != "/":
            self.send_error(404)
            return

        page = PAGE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'")
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self) -> None:
        if urlsplit(self.path).path != "/api/transform":
            self._send_json(404, {"error": "Rota não encontrada."})
            return

        try:
            body_size = int(self.headers.get("Content-Length", "0"))
            if body_size <= 0 or body_size > MAX_BODY_SIZE:
                raise ValueError("O conteúdo está vazio ou excede o limite de 1 MB.")
            payload = json.loads(self.rfile.read(body_size))
            text = payload.get("text")
            password = payload.get("password")
            mode = payload.get("mode")
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Digite ou cole um texto primeiro.")
            if not isinstance(password, str) or not password:
                raise ValueError("Informe uma senha.")
            if mode == "encrypt":
                result = encrypt_text(text, password)
            elif mode == "decrypt":
                result = decrypt_text(text, password)
            else:
                raise ValueError("Escolha criptografar ou descriptografar.")
            self._send_json(200, {"result": result})
        except (ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})

    def _send_json(self, status: int, payload: dict[str, str]) -> None:
        response = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", 8000), TextCipherHandler)
    print("Prévia disponível na porta 8000. Pressione Ctrl+C para encerrar.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
