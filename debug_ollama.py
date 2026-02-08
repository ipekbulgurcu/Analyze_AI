import requests
import sys

def check_ollama():
    url = "http://localhost:11434/api/tags"
    print(f"Checking connection to {url}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Successfully connected to Ollama!")
            print("Available models:")
            for model in response.json().get('models', []):
                print(f" - {model['name']}")
            return True
        else:
            print(f"Connected, but received status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Failed to connect: Connection Refused.")
        print("1. Please ensure Ollama is running.")
        print("2. Check if it's blocked by firewall.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    success = check_ollama()
    sys.exit(0 if success else 1)
