"""main file of project"""
import json
import os
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
DATADIR = "~/chrdrv"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"  # noqa pylint: disable=line-too-long
SRC_PAGE = "https://www.ikea.com/ru/ru/customer-service/contact-us/zayavka-na-oformlenie-zakaza-pub1a73c1b0"  # noqa pylint: disable=line-too-long
IFTTT_WEBHOOK = os.getenv("POETRY_IFTTT_WEBHOOK")


def send_notification():
    """triggers IFTTT webhook"""

    payload = json.dumps(
        {
            "value1": "<b>Форма для заказов снова доступна на сайте</b><br/>",
            "value2": SRC_PAGE,
        }
    )
    headers = {"Content-Type": "application/json"}

    requests.request("POST", IFTTT_WEBHOOK, headers=headers, data=payload)


def main():
    """main function of script"""
    ser = Service(CHROMEDRIVER_PATH)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-data-dir={DATADIR}")
    options.add_argument(f"user-agent={USER_AGENT}")

    driver = webdriver.Chrome(service=ser, options=options)

    while True:

        driver.get(SRC_PAGE)

        src = driver.page_source

        if "странице ожидания" in src:
            sleep(120)

            src = driver.page_source

            if "Прием новых заявок запустится немного позже" not in src:
                send_notification()
                with open("../page.log", "w", encoding="utf8") as file:
                    file.write(src)
                break
        else:
            if "Прием новых заявок запустится немного позже" not in src:
                send_notification()
                with open("../page.log", "w", encoding="utf8") as file:
                    file.write(src)
                break

        sleep(12)

    driver.quit()


if __name__ == "__main__":
    main()
