import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta

HOST = "localhost"
PORT = 8000

# Start time
start_time = datetime.strptime("2025-01-01T08:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

# Generate 2 hours of data (hourly)
data = []
for i in range(2):
    dt = start_time + timedelta(hours=i)
    item = {
        # test values
        "value": 1000 + i * 100,
        "units": "unitEnumSet.kwattHours",
        "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "isReliable": True
    }
    data.append(item)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        # Return the full dump
        self.wfile.write(json.dumps(data).encode("utf-8"))

if __name__ == "__main__":
    print(f"Starting mock server at http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), SimpleHandler)
    server.serve_forever()
