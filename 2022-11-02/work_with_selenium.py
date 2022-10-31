import requests
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DistanceUtil:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://map.kakao.com/"

    @staticmethod
    def convert_point_value_to_string(point_list):
        if len(point_list) == 2:
            for i, value in enumerate(point_list):
                point_list[i] = str(value)
        return point_list

    def send_button_key(self, by, value, key, clear=False):
        self.wait.until(EC.element_to_be_clickable((by, value)))
        find_button = self.driver.find_element(by, value)
        if clear:
            find_button.clear()
        find_button.send_keys(key)

    def get_text(self, by, value):
        self.wait.until(EC.element_to_be_clickable((by, value)))
        return self.driver.find_element(by, value).text

    @staticmethod
    def convert_unit_to_km(string):
        value = float(re.findall(r'[0-9.]+', string)[0])
        unit = re.findall(r'[a-z]+', string)[0]

        if unit == "m":
            return value/1000
        elif unit == "km":
            return value

    def get_distance(self, start_point, dest_point):
        """
        Input/Output Example
        Input: [33.422145, 126.278125], [33.420955, 126.273750]
        Output: {'bike': 0.502, 'walk': 0.473, 'car': 1.3}

        :param start_point: Enter the latitude and longitude of the starting point as a list.
        :param dest_point: Enter the latitude and longitude of the arrival point as a list.
        :return: Returns the distance of a bike, walk, or car route as a dictionary in km unit.
        """
        self.driver.get(self.url)

        start_point = self.convert_point_value_to_string(start_point)
        dest_point = self.convert_point_value_to_string(dest_point)

        while True:
            try:
                print("[System] Searching for paths from points {} to {}.".format(start_point, dest_point))

                self.send_button_key(By.XPATH, '//*[@id="search.keyword.query"]', ",".join(start_point) + '\n')
                self.send_button_key(By.XPATH,
                                     '/html/body/div[7]/div[6]/div[7]/div[2]/div/div[6]/div[2]/div/div[2]/div[3]/div/div[2]/button',
                                     '\n')
                self.send_button_key(By.XPATH,
                                     '/html/body/div[7]/div[6]/div[7]/div[2]/div/div[6]/div[2]/div/div[2]/div[3]/div/div[2]/div/button[1]',
                                     '\n')

                self.send_button_key(By.XPATH, '//*[@id="search.keyword.query"]', ",".join(dest_point) + '\n', clear=True)
                self.send_button_key(By.XPATH,
                                     '/html/body/div[7]/div[6]/div[7]/div[2]/div/div[6]/div[3]/div/div[2]/div[3]/div/div[2]/button',
                                     '\n')
                self.send_button_key(By.XPATH,
                                     '/html/body/div[7]/div[6]/div[7]/div[2]/div/div[6]/div[3]/div/div[2]/div[3]/div/div[2]/div/button[3]',
                                     '\n')

                distance_by_car = self.get_text(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div[5]/div[6]/ul/li/div[1]/div/div[1]/p/span[2]')

                self.send_button_key(By.XPATH,
                                     '/html/body/div[5]/div[2]/div[2]/div[2]/div/a[3]', '\n')

                distance_by_walk = self.get_text(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div[5]/div[3]/div[1]/ul/li[1]/div[1]/div/p/span[2]')

                self.send_button_key(By.XPATH,
                                     '/html/body/div[5]/div[2]/div[2]/div[2]/div/a[4]', '\n')

                distance_by_bike = self.get_text(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div[5]/div[4]/div[1]/ul/li[1]/div[1]/div[1]/p/span[2]')

                return {
                    "bike": self.convert_unit_to_km(distance_by_bike),
                    "walk": self.convert_unit_to_km(distance_by_walk),
                    "car": self.convert_unit_to_km(distance_by_car)
                }
            except Exception as e:
                print("[System] Error with {}, {}. Try again in 5 seconds.".format(start_point, dest_point), e)
                time.sleep(5)
                continue