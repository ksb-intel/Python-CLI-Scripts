import os
import socket
from datetime import datetime
from tqdm import tqdm


def scan_subdomains_pro():
    domain = input("\n[?] Enter domain (e.g., google.com): ")
    wordlist_path = "subdomains.txt"  # The file you created

    # 1. Check if the wordlist exists
    if not os.path.exists(wordlist_path):
        print(f"[X] Error: {wordlist_path} not found! Please create it first.")
        return

    # 2. Create a timestamped folder for logging
    # Format: 2023-10-27_14-30-05_google.com
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"OSINT_{domain}_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    report_path = os.path.join(folder_name, "subdomains_found.txt")

    # 3. Read the file into a list
    with open(wordlist_path, "r") as f:
        subs = [line.strip() for line in f if line.strip()]

    print(f"\n--- Scanning {len(subs)} subdomains for {domain} ---")
    print(f"--- Results will be saved in: {folder_name} ---\n")

    found_count = 0

    with open(report_path, "w") as report:
        # 4. Use tqdm for the 1,000+ items
        for sub in tqdm(subs, desc="DNS Brute Force", unit="subs"):
            full_url = f"{sub}.{domain}"
            try:
                # We use a 2-second timeout to keep things moving
                ip = socket.gethostbyname(full_url)

                result_text = f"[+] Found: {full_url} ({ip})"
                tqdm.write(result_text)  # Print to screen without breaking the bar
                report.write(result_text + "\n")  # Save to the log file
                found_count += 1

            except socket.gaierror:
                continue  # Subdomain doesn't exist, move to next

    print(f"\n[✔] Done! Found {found_count} active subdomains.")
    print(f"[✔] Full report: {report_path}")


if __name__ == "__main__":
    scan_subdomains_pro()
