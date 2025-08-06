from selenium.webdriver.common.by import By

class ProjectLocators:
    RESOURСE_MENU = (By.XPATH, '//li[@class="pushy-submenu about_menu_item pushy-submenu-closed"]')
    CONTACTS_LINKS = (By.XPATH, '//a[@id="navitem_about_contacts"]')
    CONTACTS_INFORMATION = (By.XPATH, "//*[contains(@class, 'companydata')]")
    REGION_INFORMATION = (By.XPATH, './/span[@class="region" and not(contains(., "Contact us"))]')
    COMPANIES_NAMES = (By.XPATH, './/span/b')
    ADDRESS_COMPANY = (By.XPATH, './/span[@itemprop="streetAddress"]')
    POSTAL_CODE = (By.XPATH, './/span[@itemprop="postalCode"]')
    PHONE_NUMBER = (By.XPATH, './/span[@itemprop="telephone"]')