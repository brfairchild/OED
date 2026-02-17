import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

HOST = "localhost"
PORT = 8000

# Generate some sample data
start_time = datetime.strptime("2025-01-01T08:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
mock_database = []
for i in range(5): # Generate 5 hours of data
    dt = start_time + timedelta(hours=i)
    mock_database.append({
        "value": 1000 + i * 100,
        "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "isReliable": True
    })

class MetasysMockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # --- ROUTE 1: Lookup Object ID ---
        if "/api/v3/objectIdentifiers" in parsed_path.path:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # Return a fake GUID for the FQR
            response = {"id": "550e8400-e29b-41d4-a716-446655440000"}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        # --- ROUTE 2: Get Samples ---
        elif "/samples" in parsed_path.path:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # In a real API, we'd filter by startTime/endTime here.
            # For now, we return the items in the standard v3 format.
            response = {"items": mock_database, "total": len(mock_database)}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        else:
            self.send_error(404, "Endpoint not found")

if __name__ == "__main__":
    print(f"Starting Metasys Mock Server at http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), MetasysMockHandler)
    server.serve_forever()