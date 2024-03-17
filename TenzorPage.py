from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




class TensorPage(BasePage):
    '''Class to work with page https://tensor.ru'''

    TENSOR_URL = "https://tensor.ru"
    TENSOR_URL_ABOUT = "https://tensor.ru/about"
    POWER_IN_PEOPLE_BLOCK_LOCATOR = (By.XPATH, "//p[@class='tensor_ru-Index__card-title tensor_ru-pb-16' and contains(text(), 'Сила в людях')]")
    MORE_DETAILS_LINK_LOCATOR = (By.XPATH, "(//a[@class='tensor_ru-link tensor_ru-Index__link'])[2]")
    SECTION_WORK_TOGETHER = (By.XPATH, "//h2[@class='tensor_ru-header-h2 tensor_ru-About__block-title' and contains(text(), 'Работаем')]")
    PHOTOS_LOCATOR = (By.XPATH, "//img[@class='tensor_ru-About__block3-image new_lazy loaded']")

    def __init__(self, driver):

        super().__init__(driver)


    def find_element(self,*args):

        return self.driver.find_element(*args)


    def block_strength_people_is_displayed(self):

        return self.find_element(*self.POWER_IN_PEOPLE_BLOCK_LOCATOR).is_displayed()


    def click_tensor_banner(self):
        '''Scroll and click to the banner tenzor'''

        wait = WebDriverWait(self.driver, 10)
        tensor_banner = wait.until(EC.visibility_of_element_located(self.MORE_DETAILS_LINK_LOCATOR))
        element = self.driver.find_element(*self.MORE_DETAILS_LINK_LOCATOR)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        tensor_banner.click()


    def get_elments_from_section_of_articale(self):

        element = self.driver.find_element(*self.SECTION_WORK_TOGETHER)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.PHOTOS_LOCATOR))
        images = self.driver.find_elements(*self.PHOTOS_LOCATOR)
        if len(images) > 0:
            widths = []
            heights = []
            Flag_width = True
            Flag_height = True
            for image in images:
                width = int(image.get_attribute('width'))
                height = int(image.get_attribute('height'))
                if len(widths) == 0:
                    widths.append(width)
                if len(widths) > 0:
                    if width != widths[0]:
                        Flag_width = False
                if len(heights) == 0:
                    heights.append(height)
                if len(heights) > 0:
                    if height != heights[0]:
                        Flag_height = False
            if Flag_width == True and Flag_height == True:
                return True
            else:
                return False
        else:
            return False

