import requests
import socket
import whois
from tqdm import tqdm  # Import the progress bar
import time


# --- MODULE 1: USERNAME CHECKER (UPDATED) ---
def check_username():
    username = input("\n[?] Enter username: ")
    platforms = {
        "GitHub": "https://github.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "Pinterest": "https://www.pinterest.com/{}/"
    }
    headers = {'User-Agent': 'Mozilla/5.0'}

    print(f"\nSearching for {username}...")

    # Wrap the dictionary items in tqdm for a progress bar
    # 'desc' sets the text next to the bar
    for platform, url_format in tqdm(platforms.items(), desc="Checking Platforms"):
        url = url_format.format(username)
        try:
            res = requests.get(url, headers=headers, timeout=5)
            # We print below the bar using tqdm.write to avoid breaking the animation
            if res.status_code == 200:
                tqdm.write(f"[+] FOUND: {platform}")
        except:
            tqdm.write(f"[!] ERROR: {platform}")

        time.sleep(0.5)  # Slight delay so you can actually see the bar move!


# --- MODULE 2: SUBDOMAIN SCANNER (UPDATED) ---
def scan_subdomains():
    domain = input("\n[?] Enter domain: ")
    # Expanded list for testing
    subs = ["www", "mail", "dev", "api", "admin", "test", "vps", "blog", "shop", "git"]

    print(f"\nBrute-forcing subdomains for {domain}...")
    found = []

    # Wrap the list in tqdm
    for sub in tqdm(subs, desc="Scanning DNS"):
        full_url = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full_url)
            found.append(f"{full_url} ({ip})")
        except socket.gaierror:
            continue

    print("\n--- Results ---")
    for item in found:
        print(f"[!] {item}")


# --- MODULE 3: DOMAIN & WHOIS (STAYS THE SAME) ---
def investigate_domain():
    target = input("\n[?] Enter domain: ")
    try:
        w = whois.whois(target)
        print(f"\nRegistrar: {w.registrar}\nExpires: {w.expiration_date}")
    except Exception as e:
        print(f"Error: {e}")


def main_menu():
    while True:
        print("\n1. User Check | 2. Domain Info | 3. Subdomains | 4. Exit")
        choice = input("[>] Select: ")
        if choice == "1":
            check_username()
        elif choice == "2":
            investigate_domain()
        elif choice == "3":
            scan_subdomains()
        elif choice == "4":
            break


if __name__ == "__main__":
    main_menu()
