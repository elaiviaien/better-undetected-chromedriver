import os
import time
import traceback

import undetected_chromedriver as uc_webdriver
from capsolver_extension_python import Capsolver
from cookies_manager import get_cookies
from dotenv import load_dotenv
from proxy_ext import load_proxy
from requests.exceptions import ProxyError
from selenium.common.exceptions import WebDriverException

load_dotenv()
WORKDIR = os.getenv("WORKDIR")


class UndetectedDriver:
    def __init__(self, proxy=None, profile_id=None, is_solver: bool = True, driver_version=123):
        self.proxy = proxy
        self.is_solver = is_solver
        self.profile_id = profile_id
        self.driver_version = driver_version
        self.__options = uc_webdriver.ChromeOptions()
        self._set_chromeoptions()
        self.start_and_config_driver()

    def get_driver(self):
        return self.__driver

    def _set_proxy(self, extensions_lst):
        proxy_extension_path = load_proxy(self.proxy)
        extensions_lst.append(proxy_extension_path)
        self.__options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
        self.__options.add_experimental_option('prefs', {
            'enable_do_not_track': True
        })
        preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False
        }
        self.__options.add_experimental_option("prefs", preferences)
        return extensions_lst

    def _set_capsolver(self, extentions_lst):
        capsolver_path = Capsolver(os.getenv("CAPSOLVER_TOKEN")).load().split('=')[1]
        extentions_lst.append(capsolver_path)
        return extentions_lst

    def _load_extensions(self):
        extensions_lst = []
        if self.proxy:
            extensions_lst = self._set_proxy(extensions_lst)
        if self.is_solver:
            extensions_lst = self._set_capsolver(extensions_lst)
        if extensions_lst:
            self.__options.add_argument(f"--load-extension={','.join(extensions_lst)}")

    def _set_chromeoptions(self):
        self._load_extensions()
        self.__options.add_argument('--ignore-ssl-errors=yes')
        self.__options.add_argument('--ignore-certificate-errors')
        self.__options.add_argument('--start-maximized')
        self.__options.add_argument('--no-sandbox')
        self.__options.add_argument('--disable-dev-shm-usage')
        self.__options.add_argument('--disable-setuid-sandbox')
        self.__options.add_argument('--disable-gpu')
        self.__options.add_argument('--disable-software-rasterizer')

    def __config_cdps(self):
        self.__driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;c
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        '''
        })

    def _recreate_driver(self, retry_count=0):
        self.__options = uc_webdriver.ChromeOptions()
        self._set_chromeoptions()
        return self._create_driver(retry_count + 1)

    def _create_driver(self, retry_count=0):
        try:
            if self.profile_id:
                folder_path = f'{WORKDIR}/{self.profile_id}'
                os.makedirs(folder_path, exist_ok=True)
                get_cookies(self.profile_id)
                driver = uc_webdriver.Chrome(version_main=self.driver_version,
                                             user_data_dir=folder_path,
                                             options=self.__options)
            else:
                driver = uc_webdriver.Chrome(version_main=self.driver_version,
                                             options=self.__options)
            return driver
        except (ProxyError, WebDriverException) as e:
            if retry_count < 3:
                time.sleep(20)
                print(traceback.format_exc())
                return self._recreate_driver()
            else:
                raise Exception(e)

    def start_and_config_driver(self):
        self.__driver = self._create_driver()
        self.__config_cdps()
