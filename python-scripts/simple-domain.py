import requests
import socket
import os


def investigate_domain(domain):
    # Clean the domain input (remove http:// if the user typed it)
    clean_domain = domain.replace("https://", "").replace("http://", "").split('/')[0]

    print(f"\n--- Investigating: {clean_domain} ---")

    results = {}

    # 1. Get IP Address
    try:
        ip_address = socket.gethostbyname(clean_domain)
        results['IP Address'] = ip_address
        print(f"[+] IP Address: {ip_address}")
    except socket.gaierror:
        print("[X] Could not resolve IP Address.")
        return

    # 2. Get Server Headers and Title
    try:
        url = f"https://{clean_domain}"
        response = requests.get(url, timeout=5)

        # Get the 'Server' header
        server = response.headers.get('Server', 'Unknown')
        results['Server'] = server
        print(f"[+] Server Technology: {server}")

        # Extract Page Title using basic string slicing
        content = response.text
        if "<title>" in content and "</title>" in content:
            title = content.split('<title>')[1].split('</title>')[0]
            results['Page Title'] = title
            print(f"[+] Page Title: {title}")

    except requests.exceptions.RequestException as e:
        print(f"[X] HTTP Request failed: {e}")

    # 3. Save to a simple log file
    save_report(clean_domain, results)


def save_report(domain, data):
    filename = "domain_investigations.txt"
    with open(filename, "a") as f:  # 'a' means APPEND so we don't delete old lookups
        f.write(f"\nTarget: {domain}\n")
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
        f.write("-" * 20 + "\n")
    print(f"\n[✔] Results appended to {filename}")


if __name__ == "__main__":
    target = input("Enter a domain (e.g., google.com): ")
    investigate_domain(target)

