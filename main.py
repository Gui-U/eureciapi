#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 21:42:32 2019

@author: Alecto
"""

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import yaml


def config_reader(filename: str):
    with open(filename) as file:
        documents = yaml.safe_load(file)
    return documents


def connect_to_eurecia(eurecia_host: str, login: str, password: str) -> webdriver:
    print(f"Connecting to {eurecia_host} using selenium")

    driver = webdriver.Firefox()
    driver.get("https://" + eurecia_host)

    # set the login
    element = driver.find_element_by_id("email")
    element.clear()
    element.send_keys(login)
    element.send_keys(Keys.RETURN)

    # set the password
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    element.clear()
    element.send_keys(password)
    element.send_keys(Keys.RETURN)

    # https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
    delay = 10  # seconds
    try:
        _ = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "homeRow")))
    except TimeoutException:
        print("Loading took too much time!")

    driver.get(f"https://{eurecia_host}/eurecia/payslip/Open.do")

    return driver


def driver_to_requests(driver: webdriver) -> requests.sessions.Session:
    cookies = driver.get_cookies()
    driver.close()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session


def download_last_payslip(session: requests.sessions.Session, eurecia_host: str, payslip_name: str):
    print("Download last payslip using API")
    eurecia_host = config["eurecia_host"]

    baseurl = f"https://{eurecia_host}/eurecia/api/v1/payslip"

    response = session.get(baseurl)
    if response.status_code == 200:
        payslip_list = response.json()
    else:
        print(response.content)
        raise ValueError(response.status_code)

    last_payslip_url = (
        f"https://{eurecia_host}/" + payslip_list["2020"][0]["files"][0]["urlContent"]
    )

    filename = payslip_name + payslip_list["2020"][0]["description"]
    filename = filename.replace(" ", "-")
    response = session.get(last_payslip_url)
    if response.status_code == 200:
        with open(f"{filename}.pdf", "wb") as f:
            f.write(response.content)
        print("OK")


def download_calendar(session: requests.sessions.Session, eurecia_host: str, calendar_name: str):
    print("Download calendar using API")
    eurecia_host = config["eurecia_host"]

    baseurl = f"https://{eurecia_host}/eurecia/planningVacation/planning.do?print=all"

    response = session.get(baseurl)
    if response.status_code == 200:
        calendar_raw = response.text
    else:
        print(response.content)
        raise ValueError(response.status_code)

    if response.status_code == 200:
        with open(f"{calendar_name}.txt", "w") as f:
            f.write(calendar_raw)
        print("OK")


if __name__ == "__main__":

    config = config_reader("secrets.yaml")
    driver = connect_to_eurecia(config["eurecia_host"], config["login"], config["password"])
    session = driver_to_requests(driver)
    download_last_payslip(session, config["eurecia_host"], config["payslip"])
    download_calendar(session, config["eurecia_host"], config["calendar"])
