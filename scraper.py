import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configurar logging
logging.basicConfig(level=logging.INFO)

def get_quotes(author, page):
    url = f"https://www.pensador.com/autor/{author}/{page}/"
    logging.info(f"Fetching URL: {url}")

    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.set_page_load_timeout(30)

    try:
        driver.get(url)
    except TimeoutException:
        logging.error(f"Timeout while fetching URL: {url}")
        driver.quit()
        return []

    quotes = []
    try:
        elements = driver.find_elements(By.CLASS_NAME, 'thought-card')
        for element in elements:
            try:
                quote_text = element.find_element(By.CLASS_NAME, 'frase').text.strip()
                author_name = element.find_element(By.CLASS_NAME, 'author-name').text.strip()
                quotes.append({"author": author_name, "quote": quote_text})
            except NoSuchElementException as e:
                logging.warning(f"Element not found: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()
    
    logging.info(f"Found {len(quotes)} quotes")
    return quotes
