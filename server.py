#!/usr/bin/env python3
import json, os, re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8080
PROJECT_ID = "3936815"

WIDGETS_DATA = json.load(open("api/widgets-combined.json"))
print(f"Loaded {len(WIDGETS_DATA)} widgets")

ServerData = json.loads(open("index.html").read().split("window.ServerData =")[1].split("</script>")[0].strip().rstrip(";"))
PAGES = ServerData["mags"]["mag"]["pages"]
PAGE_WIDS = {p["_id"]: set(p.get("wids", [])) for p in PAGES}
print(f"Loaded {len(PAGES)} pages from ServerData")

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if re.match(r'/api/viewer/project/\d+/widgets', path):
            page_id = query.get("pageId", [None])[0]
            if page_id and page_id in PAGE_WIDS:
                allowed_wids = PAGE_WIDS[page_id]
                filtered = [w for w in WIDGETS_DATA if w.get("wid") in allowed_wids]
                print(f"  -> Widgets for page {page_id[:12]}...: {len(filtered)}/{len(WIDGETS_DATA)}")
                self._json_response(filtered)
            else:
                print(f"  -> All widgets ({len(WIDGETS_DATA)})")
                self._json_response(WIDGETS_DATA)
            return

        if path in ("/api/fonts/typetoday/css", "/api/fonts/typetoday/css.css"):
            self._serve_css("api/fonts/typetoday/css.css", "typetoday")
            return

        if path in ("/api/fonts/webtype/css", "/api/fonts/webtype/css.css"):
            self._serve_css("api/fonts/webtype/css.css", "webtype")
            return

        if re.match(r'/api/fonts/[a-f0-9]+/css$', path):
            css_path = "api/fonts/custom/css.css"
            if os.path.exists(css_path):
                self._serve_css(css_path, "custom")
            else:
                self._ok_response(b"/* empty */", "text/css")
            return

        if "/api/countview/" in path:
            self._ok_response(b"ok", "text/plain")
            return

        if "/api/proxy/" in path:
            self._json_response({"status": 200})
            return

        super().do_GET()

    def _json_response(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _ok_response(self, body, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_css(self, filepath, label):
        if os.path.exists(filepath):
            with open(filepath) as f:
                body = f.read().encode("utf-8")
            self._ok_response(body, "text/css")
            print(f"  -> Font CSS: {label}")
        else:
            self._ok_response(b"/* empty */", "text/css")

    def log_message(self, format, *args):
        if 'api/' in self.path:
            print(f"[API] {args[0]} {args[1]} {args[2]}")

if __name__ == "__main__":
    server = HTTPServer(("", PORT), Handler)
    print(f"Server running at http://localhost:{PORT}")
    print(f"Widget API: http://localhost:{PORT}/api/viewer/project/{PROJECT_ID}/widgets")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
