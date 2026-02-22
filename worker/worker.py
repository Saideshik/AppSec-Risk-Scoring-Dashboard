import os, time, requests

API = os.environ.get("API_BASE_URL", "http://backend:8000")

def main():
    while True:
        try:
            r = requests.post(f"{API}/metrics/recalc", timeout=10)
            print("recalc:", r.status_code, r.text)
        except Exception as e:
            print("recalc error:", e)

        # every 6 hours
        time.sleep(6 * 60 * 60)

if __name__ == "__main__":
    main()
