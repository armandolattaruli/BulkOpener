from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def open_ip_links(ip_list):
    base_urls = [
        "https://www.virustotal.com/gui/ip-address/{}",
        "https://www.abuseipdb.com/check/{}"
    ]
    
    options = Options()
    # Remove headless mode to see the browser opening
    # options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get("https://www.google.com")  # Open an initial tab
    
    for ip in ip_list.split("\n"):
        ip = ip.strip()
        if ip:
            for url in base_urls:
                new_tab_script = f"window.open('{url.format(ip)}', '_blank');"
                driver.execute_script(new_tab_script)
                time.sleep(2)  # Allow page to load
    
    driver.quit()  # Close the browser after finishing

# Example usage:
ip_addresses = """192.168.1.1
8.8.8.8
1.1.1.1"""
open_ip_links(ip_addresses)
