import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService

url = "https://www.theses.fr/en/?q=*:*&lng=en&start=0&status=&access=&prevision=&filtrepersonne="

chrome_service = ChromeService("/Users/ayoub/Downloads/chromedriver-mac-x64/chromedriver" , port=9516)  
driver = webdriver.Chrome(service=chrome_service)
driver.get(url)

driver.implicitly_wait(10)

# Créer un fichier CSV pour stocker les données
with open("theses.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Titre", "Auteur", "Subject"])

    while True:
        thesis_links = driver.find_elements(By.CSS_SELECTOR , "div.informations h2 a")
        if not thesis_links:
            break

        # Boucle à travers les liens et accédez aux pages de détails
        for thesis_link in thesis_links:
            # Cliquez sur le lien pour accéder aux détails de la thèse
            ActionChains(driver).move_to_element(thesis_link).click().perform()

            # Attendre que la page de détails se charge complètement
            driver.implicitly_wait(10)

            # Extraire les informations de la page de détails
            title = driver.find_element(By.CSS_SELECTOR, "h1").text
            author = driver.find_element(By.CSS_SELECTOR, "h2 span").text
            subject = driver.find_element(By.CSS_SELECTOR, "div.these_soutenue p span, div.these_preparation p span").text

            # Écrire les informations dans le fichier CSV
            csv_writer.writerow([title, author, subject])

            driver.back()

        # Passer à la page suivante
        next_page_element = driver.find_element(By.CSS_SELECTOR, "a[href*='start'] img[alt='Page suivante']")
        ActionChains(driver).move_to_element(next_page_element).click().perform()

# Fermer le navigateur
driver.quit()

