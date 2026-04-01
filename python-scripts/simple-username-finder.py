import requests
import time
import random

## Randomly selects the header to avoid being considered bot traffic
def random_header():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": 'en-US,en;q=0.9',
    }

## function to check the username
def username_finder(username):
    platforms = {
        "GitHub": "https://github.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}/",
        "Reddit": "https://www.reddit.com/user/{}",
        "Pinterest": "https://www.pinterest.com/{}/",
        "TikTok": "https://www.tiktok.com/@{}",
    }

    print(f"--- Advanced Search for: {username} ---\n")

    for platform, url_format in platforms.items():
        url = url_format.format(username)

        current_header = random_header()

        try:
            # Pass the random headers into the get() function here
            response = requests.get(url, headers=current_header, timeout=5)

            if response.status_code == 200:
                print(f"[!] {platform}: Profile Found! -> {url}")
            elif response.status_code == 404:
                print(f"[-] {platform}: Available (404)")
            elif response.status_code == 403:
                print(f"[X] {platform}: Access Denied (403) - Site is blocking the script.")
            else:
                print(f"[?] {platform}: Status {response.status_code}")

            # Pause for 2 seconds between requests
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"[X] {platform}: Connection Error.")


# asks the user to input the username, then runs username_finder against the inputted user
if __name__ == "__main__":
    target_user = input("Who is the user?").strip()
    username_finder(target_user)