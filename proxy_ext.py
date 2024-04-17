import os
import zipfile
from dotenv import load_dotenv

load_dotenv()
WORKDIR = os.getenv("WORKDIR")


def load_proxy(proxy):
    PROXY_HOST = proxy.replace('https://', '').replace('http://', '').split('@')[1].split(':')[0]
    PROXY_PORT = proxy.replace('https://', '').replace('http://', '').split('@')[1].split(':')[1]
    PROXY_USER = proxy.replace('https://', '').replace('http://', '').split('@')[0].split(':')[0]
    PROXY_PASS = proxy.replace('https://', '').replace('http://', '').split('@')[0].split(':')[1]
    print(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
   callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    pluginfile = 'proxy_auth_plugin' + str(hash(proxy))
    base_path = f'{WORKDIR}/proxies/'
    with zipfile.ZipFile(base_path + pluginfile + ".zip", 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    # create dir
    os.makedirs(base_path + pluginfile, exist_ok=True)
    with zipfile.ZipFile(base_path + pluginfile + ".zip") as zp:
        zp.extractall(base_path + pluginfile)
    return base_path + pluginfile
