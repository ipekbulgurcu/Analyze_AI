import requests
import sys
import os

BASE_URL = "http://127.0.0.1:8000"

def log(message, success=True):
    symbol = "✅" if success else "❌"
    print(f"{symbol} {message}")

def verify_features():
    print("Starting Feature Verification...\n")
    all_passed = True

    # 1. Check Health
    try:
        resp = requests.get(f"{BASE_URL}/health")
        if resp.status_code == 200:
            log("Health Check Passed")
        else:
            log(f"Health Check Failed: {resp.status_code}", False)
            all_passed = False
    except Exception as e:
        log(f"Health Check Error: {e}", False)
        return False

    # 2. Check Frontend
    try:
        resp = requests.get(f"{BASE_URL}/")
        if resp.status_code == 200 and "<title>Yinov AI" in resp.text:
            log("Frontend Serving Passed")
        else:
            log(f"Frontend Check Failed: {resp.status_code}", False)
            all_passed = False
    except Exception as e:
        log(f"Frontend Check Error: {e}", False)
        all_passed = False

    # 3. Check Ingestion
    dummy_file = "test_doc.txt"
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write("Yinov AI is a powerful document assistant developed to help users analyze PDFs.")
    
    try:
        with open(dummy_file, "rb") as f:
            files = {"file": (dummy_file, f, "text/plain")}
            resp = requests.post(f"{BASE_URL}/ingest", files=files)
            
        if resp.status_code == 200:
            data = resp.json()
            if data.get("chunks_count", 0) > 0:
                log(f"Ingestion Passed (Chunks: {data['chunks_count']})")
            else:
                log("Ingestion Failed: No chunks created", False)
                all_passed = False
        else:
            log(f"Ingestion Failed: {resp.status_code} - {resp.text}", False)
            all_passed = False
    except Exception as e:
        log(f"Ingestion Error: {e}", False)
        all_passed = False
    finally:
        if os.path.exists(dummy_file):
            os.remove(dummy_file)

    # 4. Check QA (Ask)
    try:
        payload = {"query": "What is Yinov AI?"}
        resp = requests.post(f"{BASE_URL}/ask", json=payload)
        
        if resp.status_code == 200:
            data = resp.json()
            answer = data.get("answer", "")
            if answer:
                log(f"QA Passed. Answer length: {len(answer)}")
                print(f"   > Question: What is Yinov AI?")
                print(f"   > Answer: {answer.strip()[:100]}...")
            else:
                log("QA Failed: Empty answer", False)
                all_passed = False
        else:
            log(f"QA Failed: {resp.status_code} - {resp.text}", False)
            all_passed = False
    except Exception as e:
        log(f"QA Error: {e}", False)
        all_passed = False

    print("\nVerification Complete.")
    return all_passed

if __name__ == "__main__":
    success = verify_features()
    sys.exit(0 if success else 1)
