import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        names = query.get('name', [])

        try:
            # Load JSON data
            json_path = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')
            with open(json_path, 'r') as f:
                raw_data = json.load(f)

            # Convert list to dict: {"Alice": 10, "Bob": 20}
            data = {entry['name']: entry['marks'] for entry in raw_data}

            # Lookup marks
            marks = [data.get(name, 0) for name in names]

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"marks": marks}).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
