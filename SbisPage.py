import os
from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep




class SbisPage(BasePage):
    '''Class to work with page of site https://sbis.ru/'''

    SBIS_URL = "https://sbis.ru/"
    SBIS_BANNER_LOCATOR = (By.XPATH, "//a[@class='sbisru-Header__menu-link sbisru-Header__menu-link--hover' and contains(text(), 'Контакты')]")
    SBIS_BANNER_TENZOR_LOCATOR = (By.XPATH, "//a[@class='sbisru-Contacts__logo-tensor mb-12']")
    SBIS_REGION_NAME = (By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    SBIS_REGION_POPUP = (By.XPATH, "//div[@class='sbis_ru-Region-Panel__container']")
    SBIS_REGIONS_NAMES = (By.XPATH, "//span[@class='sbis_ru-link']")
    SBIS_DOWNLOAD = (By.XPATH, '//a[@class="sbisru-Footer__link" and contains(text(), "Скачать локальные версии")]')
    SBIS_PLUGIN = (By.XPATH, " //div[@class='controls-TabButton controls-TabButton__right-align controls-ListView__item undefined ws-enabled ws-control-inactive ws-component']")
    SBIS_WINDOWS = (By.XPATH, '//span[''@class="sbis_ru-DownloadNew-innerTabs__title '
                        'sbis_ru-DownloadNew-innerTabs__title--default" and contains(text(), "Windows")]')
    SBIS_FILE_DOWNLOAD = (By.XPATH, "(//a[@class='sbis_ru-DownloadNew-loadLink__link js-link'])[11]")


    def __init__(self, driver):

        super().__init__(driver)


    def find_element(self, element):

        if element == 'контакты':
            return self.driver.find_element(*self.SBIS_BANNER_LOCATOR)
        elif element == 'тензор':
            return self.driver.find_element(*self.SBIS_BANNER_TENZOR_LOCATOR)
        else:
            raise ValueError("укажите наименование элемента для поиска")


    def buttom_is_display(self, element):

        if element == 'контакты' or element == 'тензор':
            return self.find_element(element).is_displayed()
        else:
            raise ValueError("укажите наименование элемента для поиска")


    def click_button(self, element):

        if element == 'контакты' or element == 'тензор':
            self.find_element(element).click()
        else:
            raise ValueError("укажите наименование элемента для поиска")


    def get_attribute_href(self, element):

        if element == 'контакты' or element == 'тензор':
            return self.find_element(element).get_attribute("href")
        else:
            raise ValueError("укажите наименование элемента для поиска")


    def find_other_element(self,*args):

        return self.driver.find_element(*args)


    def check_region(self):

        region = self.find_other_element(*self.SBIS_REGION_NAME)
        return region.text


    def change_region(self):

        my_region = self.find_other_element(*self.SBIS_REGION_NAME)
        my_region.click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.SBIS_REGIONS_NAMES))
        regions_name_list = self.driver.find_elements(*self.SBIS_REGIONS_NAMES)
        for popup_region in regions_name_list:
            if popup_region.text == "41 Камчатский край":
                popup_region.click()
                sleep(3)
                break


    def get_directory(self):

        download_directory = f'{os.getcwd()}\\Downloads'
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)
        return download_directory


    def click_to_page_download(self):

        self.open_page(self.SBIS_URL)
        element = self.driver.find_element(*self.SBIS_DOWNLOAD)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        link = self.find_other_element(*self.SBIS_DOWNLOAD)
        link.click()


    def download_file(self):

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.SBIS_PLUGIN))
        self.driver.find_element(*self.SBIS_PLUGIN).click()
        self.driver.find_element(*self.SBIS_WINDOWS).click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.SBIS_FILE_DOWNLOAD))
        buttom = self.driver.find_element(*self.SBIS_FILE_DOWNLOAD)
        text_link = buttom.text
        buttom.click()
        sleep(10)
        return text_link


    def check_downloading_file_in_directory(self, text_link):

        numbers = '.0123456789'
        start = -1
        count = 0
        for i in range(len(text_link) - 1):
            if text_link[i] in numbers and start == -1:
                start = i
            if text_link[i] in numbers:
                count += 1
        end = start + count
        size_number = float(text_link[start:end])

        directory = self.get_directory()
        files = os.listdir(directory)
        list_size_files = []
        for file in files:
            file_size = os.path.getsize(f'{directory}\\{file}')
            file_size_kb = file_size / 1024
            file_size_mb = file_size_kb / 1024
            list_size_files.append(round(file_size_mb, 2))
        print(*list_size_files)
        if size_number in list_size_files:
            return True
        else:
            return False



