import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def open_ip_links(file_path, output_file="positives.txt"):
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
        with open(file_path, "r") as file, open(output_file, "a") as out_file:
            for ip in file:
                ip = ip.strip()
                if ip:
                    # Open VirusTotal and AbuseIPDB in new tabs
                    vt_url = base_urls[0].format(ip)
                    abuse_url = base_urls[1].format(ip)
                    driver.execute_script(f"window.open('{vt_url}', '_blank');")
                    driver.execute_script(f"window.open('{abuse_url}', '_blank');")
                    time.sleep(2)  # Allow pages to load
                    
                    driver.switch_to.window(driver.window_handles[-2])  # Switch to VirusTotal tab
                    try:
                        positives_element = driver.find_element(By.ID, "positives")
                        positives = int(positives_element.text.strip())
                        if positives > 0:
                            out_file.write(f"{ip} - {vt_url}\n")
                    except:
                        print(f"Could not find positives data for {ip}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    
    print("Browser will remain open. Close it manually when done.")
    try:
        driver.wait_for_window_to_close()
    except:
        pass  # Exit loop if the browser is closed

    print("Browser closed. Exiting script.")
    os._exit(0)  # Forcefully exit the script when the browser is closed

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_ip_file>")
    else:
        open_ip_links(sys.argv[1])
