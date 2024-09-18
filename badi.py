
import csv
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def get_guest_count(url):
    
    # Path to ChromeDriver
    chrome_driver_path = "/usr/bin/chromedriver"

    # Initialize Chrome WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open the URL
        driver.get(url)
        
        # Wait for the "Anzahl Gäste" element to load (with a timeout of 10 seconds)
        wait = WebDriverWait(driver, 10)
        guest_count_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Anzahl Gäste')]")))
        
        # Get the sibling element containing the guest count
        guest_count_value = guest_count_element.find_element(By.XPATH, "following-sibling::*").text.strip()
        
        # Try converting the guest count to an integer
        try:
            return int(guest_count_value)
        except ValueError:
            raise ValueError(f"Could not convert '{guest_count_value}' to an integer.")
    
    finally:
        # Close the browser window
        driver.quit()

    return guest_count

def main():
    url = "https://www.stadt-zuerich.ch/ssd/de/index/sport/schwimmen/hallenbaeder/hallenbad_city.html"

    # Get and print the guest count
    guest_count = get_guest_count(url)
    print(url, guest_count)
    
    # Write to CSV
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('data/swimmers.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, url, guest_count])

    print(f"Data written to CSV: {timestamp}, {url}, {guest_count}")

if __name__ == "__main__":
    main()


