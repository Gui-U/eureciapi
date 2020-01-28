#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jar 27 21:42:32 2019

@author: Alecto
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import yaml
import time

def config_reader(filename :str):    
    with open(filename) as file:
        documents = yaml.safe_load(file)
    return documents

def connect_to_eurecia(eurecia_host :str, login :str, password :str) -> webdriver:
    print(f"Connecting to {eurecia_host}...")
    
    driver = webdriver.Firefox()
    driver.get("https://" + eurecia_host)
    
    # set the login
    element = driver.find_element_by_id("email")
    element.clear()
    element.send_keys(login)
    element.send_keys(Keys.RETURN)
    
    
    # set the password
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.clear()
    element.send_keys(password)
    element.send_keys(Keys.RETURN)
    
    
#    try:
#        wait = WebDriverWait(driver, 10)
#        wait.until(EC.presenceOfElementLocated(By.tagName('topMenuButton')))
#        print(f"Your are connected !")
#    except :
#        raise Exception("You seems not connected...")
        
    return driver


def download_last_fichedepaie(driver: webdriver, eurecia_host:str):
    print("Download last fichedepaie")
    

    time.sleep(5)
#    # Go to download page
#    element = driver.find_element_by_link_text("Feuille en cours")
#    element.click()
#

    driver.get("https://" + eurecia_host + "/eurecia/hrpack/directoryUser/Browse.do")

    


    return driver

if __name__ == "__main__":
    
    config = config_reader("secrets.yaml")
    driver =        connect_to_eurecia(config['eurecia_host'],config['login'],config['password'])
    driver =download_last_fichedepaie(driver, config['eurecia_host'])