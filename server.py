import http.server
import json
import os
import socketserver

PORT = 8765
EXPECTED_HEADER = ["日付", "商品名", "カテゴリ", "地域", "数量", "単価", "売上金額"]


def is_matching_csv(name):
    if not name.lower().endswith(".csv"):
        return False
    try:
        with open(name, encoding="utf-8") as f:
            header = f.readline().strip().split(",")
    except OSError:
        return False
    return header == EXPECTED_HEADER


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/csvs":
            self.send_csv_list()
        else:
            super().do_GET()

    def send_csv_list(self):
        files = sorted(name for name in os.listdir(".") if is_matching_csv(name))
        body = json.dumps(files, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"serving {os.getcwd()} on http://127.0.0.1:{PORT}")
        httpd.serve_forever()
