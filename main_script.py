from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from locators import ProjectLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# 1. В данной функции мы проверяем, есть ли каждое поле в каждой компании(например, у Сингапура нет 'postcode'). Если поля нет, то записываем ''
def get_text(office, locator):
    try:
        return office.find_element(*locator).text.strip()
    except:
        return ''

def parse_contacts(output_file_path):
    service = Service(executable_path="C:/Tools_firefox/geckodriver.exe")
    options = Options()
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # 2. Открываем браузер
        driver.get("https://www.onlyoffice.com")

        # 3. Ждем загрузку страницы и наводим курсор на 'Resources'
        resources_menu = wait.until(EC.element_to_be_clickable(ProjectLocators.RESOURСE_MENU))
        ActionChains(driver).move_to_element(resources_menu).perform()

        # 4. Кликаем на "Contacts"
        contacts_link = wait.until(EC.element_to_be_clickable(ProjectLocators.CONTACTS_LINKS))
        contacts_link.click()

        # 5. Ждем загрузку карточек компаний
        wait.until(EC.presence_of_all_elements_located(ProjectLocators.CONTACTS_INFORMATION))
        office_blocks = driver.find_elements(*ProjectLocators.CONTACTS_INFORMATION)

        # 6. Создаем список, в который записываем информацию о каждой компании
        parsed_data = []

        # 7. В данном цикле мы вызываем функцию get_text, проверяем наличия поля и записываем в список parsed_data
        for office in office_blocks:
            country = get_text(office, ProjectLocators.REGION_INFORMATION)
            company_name = get_text(office, ProjectLocators.COMPANIES_NAMES)
            address = get_text(office, ProjectLocators.ADDRESS_COMPANY)
            postal_code = get_text(office, ProjectLocators.POSTAL_CODE)
            phone_number = get_text(office, ProjectLocators.PHONE_NUMBER)

            if not (country or company_name):
                continue

            parsed_data.append([country, company_name, address, postal_code, phone_number])

        # 8. Записываем данные в csv файл
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['Country', 'CompanyName', 'FullAddress', 'PostalCode', 'PhoneNumber'])
            writer.writerows(parsed_data)

        print(f"Данные сохранены в файл: {output_file_path}")

        # 9. Закрываем браузер
    finally:
        driver.quit()

parse_contacts('contacts.csv')
