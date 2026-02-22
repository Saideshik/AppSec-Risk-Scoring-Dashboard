import os, json, requests

API = os.environ.get("API_BASE_URL", "http://localhost:8000")

def main():
    path = os.path.join(os.path.dirname(__file__), "findings_mock.jsonl")
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            payload = json.loads(line)
            r = requests.post(f"{API}/findings", json=payload, timeout=10)
            print(r.status_code, r.text)

    r = requests.post(f"{API}/metrics/recalc", timeout=10)
    print("recalc:", r.status_code, r.text)

if __name__ == "__main__":
    main()
