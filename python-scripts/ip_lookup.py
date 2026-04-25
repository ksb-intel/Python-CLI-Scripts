import requests

def lookup_ip(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"

    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'success':
            print(f"\n--- Results for {ip_address} ---")
            print(f"Country:   {data.get('country')}")
            print(f"Region:    {data.get('regionName')}")
            print(f"City:      {data.get('city')}")
            print(f"Zip Code:  {data.get('zip')}")
            print(f"ISP:       {data.get('isp')}")
            print(f"Lat/Long:  {data.get('lat')}, {data.get('lon')}")
            print("-" * 30)
        else:
            print(f"Error: Unable to retrieve data for {ip_address}. Message: {data.get('message')}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    target_ip = input("Enter IP address: ")
    lookup_ip(target_ip)