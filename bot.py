from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Ścieżka do pliku JSON z ciasteczkami
cookies_path = 'C:\\Users\\lukas\\Desktop\\instagram.json'

# Konfiguracja drivera
driver = webdriver.Chrome()  # ZChrome logon
driver.get('https://instagram.com')

# Wczytanie ciasteczek z pliku JSON
with open(cookies_path, 'r') as cookies_file:
    cookies = json.load(cookies_file)
    for cookie in cookies:
        # Sprawdź, czy ciasteczko ma atrybut 'sameSite', jeśli nie, dodaj domyślną wartość 'Lax'
        if 'sameSite' not in cookie or cookie['sameSite'] not in ["Strict", "Lax", "None"]:
            cookie['sameSite'] = 'Lax'
        driver.add_cookie(cookie)

# Odśwież stronę, aby ciasteczko zostało użyte
driver.refresh()

try:
    # Oczekiwanie na załadowanie pola wyszukiwania
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Pole wejściowe wyszukiwania"]'))
    )
    search_field = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Pole wejściowe wyszukiwania"]')
    search_field.send_keys("#truckcranes")
    search_field.send_keys(Keys.RETURN)

    # Oczekiwanie na wyniki i wybór użytkownika
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user_link"))
    )
    user_links = driver.find_elements(By.CLASS_NAME, "user_link")
    user_links[0].click()

    # Przejdź do obserwujących
    followers_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "followers_link"))
    )
    followers_link.click()

    # Oczekiwanie na zdjęcia i polubienie
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "photo"))
    )
    photos = driver.find_elements(By.CLASS_NAME, "photo")
    for photo in photos[:5]:  # Polub maksymalnie 5 zdjęć
        like_button = photo.find_element(By.CLASS_NAME, "like_button")
        like_button.click()
        time.sleep(2)  # Czekaj 2 sekundy między polubieniami

finally:
    driver.quit()  # Zamknij przeglądarkę na końcu
