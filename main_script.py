from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from locators import ProjectLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import csv

def get_text(office, locator):
    try:
        return office.find_element(*locator).text.strip()
    except:
        return ''

def parse_contacts(output_file_path):

    if not output_file_path.lower().endswith('.csv'):
        raise ValueError("Неверный формат файла. Ожидается .csv")
    options = Options()
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.onlyoffice.com")

        resources_menu = wait.until(EC.element_to_be_clickable(ProjectLocators.RESOURСE_MENU))
        ActionChains(driver).move_to_element(resources_menu).perform()

        contacts_link = wait.until(EC.element_to_be_clickable(ProjectLocators.CONTACTS_LINKS))
        contacts_link.click()

        wait.until(EC.presence_of_all_elements_located(ProjectLocators.CONTACTS_INFORMATION))
        office_blocks = driver.find_elements(*ProjectLocators.CONTACTS_INFORMATION)

        parsed_data = []

        for office in office_blocks:
            country = get_text(office, ProjectLocators.REGION_INFORMATION)
            company_name = get_text(office, ProjectLocators.COMPANIES_NAMES)
            address = get_text(office, ProjectLocators.ADDRESS_COMPANY)
            postal_code = get_text(office, ProjectLocators.POSTAL_CODE)
            phone_number = get_text(office, ProjectLocators.PHONE_NUMBER)

            if not (country or company_name):
                continue

            parsed_data.append([country, company_name, address, postal_code, phone_number])

        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['Country', 'CompanyName', 'FullAddress', 'PostalCode', 'PhoneNumber'])
            writer.writerows(parsed_data)

        print(f"Данные сохранены в файл: {output_file_path}")

    finally:
        driver.quit()

parse_contacts('contacts.csv')