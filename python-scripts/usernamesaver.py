import requests
import time
import csv


def check_and_save_osint(username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    platforms = {
        "GitHub": "https://github.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}/",
        "Reddit": "https://www.reddit.com/user/{}"
    }

    filename = f"{username}_report.csv"

    # 'w' creates the file, newline='' prevents empty rows in CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Platform", "Status", "URL"])

        print(f"--- Generating Report for: {username} ---")

        for platform, url_format in platforms.items():
            url = url_format.format(username)
            status_text = "Unknown"

            try:
                response = requests.get(url, headers=headers, timeout=5)

                if response.status_code == 200:
                    status_text = "Found"
                    print(f"[!] {platform}: Found")
                elif response.status_code == 404:
                    status_text = "Available"
                    print(f"[-] {platform}: Not Found")
                else:
                    status_text = f"Error {response.status_code}"
                    print(f"[?] {platform}: {status_text}")

                # Write the result to the CSV file
                writer.writerow([platform, status_text, url])

                time.sleep(1)  # Be polite to servers

            except requests.exceptions.RequestException:
                writer.writerow([platform, "Connection Error", url])
                print(f"[X] {platform}: Connection Error")

    print(f"\n[✔] Search complete. Results saved to: {filename}")


if __name__ == "__main__":
    user_to_check = input("Enter a username to search: ")
    check_and_save_osint(user_to_check)