from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




class BasePage:
    '''Base class to be opening page and switch to new window'''


    def __init__(self, driver):
        self.driver = driver


    def open_page(self, url):

        self.driver.get(url)


    def get_current_url(self):

        return self.driver.current_url


    def switch_to_new_window(self):
        '''The function before get handle after switch to other opening
        window'''

        current_window_handle = self.driver.current_window_handle
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.number_of_windows_to_be(2))
        all_window_handles = self.driver.window_handles
        for window_handle in all_window_handles:
            if window_handle != current_window_handle:
                self.driver.switch_to.window(window_handle)
                return window_handle
        raise RuntimeError("Не удалось переключиться на новое окно")