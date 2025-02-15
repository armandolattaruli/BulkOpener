import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def open_ip_links(file_path):
    base_urls = [
        "https://www.virustotal.com/gui/ip-address/{}",
        "https://www.abuseipdb.com/check/{}"
    ]
    
    options = Options()
    # Remove headless mode to see the browser opening
    # options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get("https://www.google.com")  # Open an initial tab
    
    try:
        with open(file_path, "r") as file:
            for ip in file:
                ip = ip.strip()
                if ip:
                    for url in base_urls:
                        new_tab_script = f"window.open('{url.format(ip)}', '_blank');"
                        driver.execute_script(new_tab_script)
                        time.sleep(0.5)  # Allow page to load
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_ip_file>")
    else:
        open_ip_links(sys.argv[1])
