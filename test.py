import pytest
from selenium import webdriver
from TenzorPage import TensorPage
from SbisPage import SbisPage
from selenium.webdriver.chrome.options import Options
import logging
import os





def init_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    format = '%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s'
    file_handler = logging.FileHandler(filename='logs\\test.log',
                                       encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(format))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(format))
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.addHandler(stream_handler)
    return logger

logger = init_logger(__name__)


@pytest.fixture(scope="module")
def browser():
    '''The function add options browser in driver and create driver'''

    download_directory = f'{os.getcwd()}\\Downloads'
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    project_directory = download_directory
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': project_directory,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    # Создание экземпляра драйвера с опциями
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

# Задание№1
def test_sbis_page_button_contacts_exists(browser):
    """Checking the element exist"""

    logger.debug('start test_sbis_page_button_contacts_exists')
    sbis_page = SbisPage(browser)
    sbis_page.open_page(SbisPage.SBIS_URL)
    assert sbis_page.buttom_is_display('контакты'), 'The element exists on ' \
                                                    'the page'
    logger.debug('Assertion passed: button Контакты exists on the page')

def test_sbis_page_button_contacts_click(browser):
    """To check the transition to the 'Контакты' section"""

    logger.debug('start test_sbis_page_button_contacts_exists')
    sbis_page = SbisPage(browser)
    sbis_page.open_page(SbisPage.SBIS_URL)
    href = sbis_page.get_attribute_href('контакты')
    sbis_page.click_button('контакты')
    current_url = sbis_page.get_current_url()
    assert href in current_url, 'Assertion failed: link is not current url'
    logger.debug('Assertion passed: link is correctly')


def test_sbis_page_banner_tenzor_click(browser):
    """Checking the URL after clicking on the link"""

    logger.debug('Start test_block_power_people_exsits')
    sbis_page = SbisPage(browser)
    sbis_page.open_page(SbisPage.SBIS_URL)
    sbis_page.click_button('контакты')
    if not sbis_page.buttom_is_display('тензор'):
        assert sbis_page.buttom_is_display('контакты'), 'The element exists on the page'
    href = sbis_page.get_attribute_href('тензор')
    sbis_page.click_button('тензор')
    sbis_page.switch_to_new_window()
    current_url = sbis_page.get_current_url()
    assert href == current_url, 'Assertion failed: current url failed'
    logger.debug('Assertion passed: url correctly')


def test_block_power_people_exsits(browser):
    '''Сhecks for the presence of a block on the page'''

    logger.debug('Start test_block_power_people_exsits')
    tensor_page = TensorPage(browser)
    tensor_page.open_page(tensor_page.TENSOR_URL)
    assert tensor_page.block_strength_people_is_displayed(), 'Assertion failed: блок сильные люди отусутствует'
    logger.debug('Assertion passed: block exists on the page')

def test_block_power_people_click(browser):
    """Checking the URL after clicking on the link"""

    logger.debug('start test_block_power_people_click')
    tensor_page = TensorPage(browser)
    tensor_page.open_page(tensor_page.TENSOR_URL)
    tensor_page.click_tensor_banner()
    url = tensor_page.get_current_url()
    assert 'https://tensor.ru/about' == url, 'Assertion failed: url is failed'
    logger.debug('Assertion passed: url is correctly')


def test_size_photos(browser):
    """Checking size all the photos in the block"""

    logger.debug('Start test_size_photos')
    tensor_page = TensorPage(browser)
    tensor_page.open_page(tensor_page.TENSOR_URL_ABOUT)
    result = tensor_page.get_elments_from_section_of_articale()
    assert result == True, 'Assertion failed: size failed'
    logger.debug('Assertion passed: sizes of photos are correctly')

# Задание№2
def test_check_region(browser):
    """Checking your region"""

    logger.debug('Start test_check_region')
    sbis_page = SbisPage(browser)
    sbis_page.open_page(SbisPage.SBIS_URL)
    sbis_page.click_button('контакты')
    name_region = sbis_page.check_region()
    assert name_region == 'Республика Татарстан', 'Assertion failed: region ' \
                                                  'failed'
    logger.debug('Assertion passed: region is correctly')


def test_change_region(browser):
    '''To change region'''

    logger.debug('Старт теста Проверка изменение региона')
    sbis_page = SbisPage(browser)
    sbis_page.open_page(SbisPage.SBIS_URL)
    sbis_page.click_button('контакты')
    sbis_page.change_region()
    name_region = sbis_page.check_region()
    assert name_region == 'Камчатский край', 'Assertion failed: region failed'
    logger.debug('Assertion passed: region изменен на Камчатский край')

#Задание3

def test_sbis_downloads(browser):
    """Check function Downloaded file and check it in the director"""

    logger.debug('Start test_sbis_downloads')
    sbis_page = SbisPage(browser)
    logger.info("Clicking to download page")
    sbis_page.click_to_page_download()
    text_link = sbis_page.download_file()
    assert sbis_page.check_downloading_file_in_directory(text_link), \
        'Assertion failed: file have not downloaded'
    logger.debug('Assertion passed: file downloaded and size of file is '
                 'correctly')





