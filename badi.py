from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_guest_count(url):
    # Path to the local ChromeDriver
    chrome_driver_path = './chromedriver'  # Update if using a different path
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    
    # Set up the WebDriver service with the path to the local ChromeDriver
    service = Service(executable_path=chrome_driver_path)
    
    # Initialize WebDriver with the specified options and service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open the URL
        driver.get(url)
        
        # Wait for the "Anzahl Gäste" element to load (with a timeout of 10 seconds)
        wait = WebDriverWait(driver, 10)
        guest_count_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Anzahl Gäste')]")))
        
        # Get the sibling element containing the guest count
        guest_count_value = guest_count_element.find_element(By.XPATH, "following-sibling::*").text.strip()
        
        # Check if the guest count is available
        if guest_count_value == '-':
            return None  # or return 0 if you prefer
        
        # Try converting the guest count to an integer
        try:
            return int(guest_count_value)
        except ValueError:
            raise ValueError(f"Could not convert '{guest_count_value}' to an integer.")
    
    finally:
        # Close the browser window
        driver.quit()

# URL to scrape
url = "https://www.stadt-zuerich.ch/ssd/de/index/sport/schwimmen/hallenbaeder/hallenbad_city.html"

# Get and print the guest count
guest_count = get_guest_count(url)
if guest_count is not None:
    print(f"Anzahl Gäste: {guest_count}")
else:
    print("Anzahl Gäste is not available.")
