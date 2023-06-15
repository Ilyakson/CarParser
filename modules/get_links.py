import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from django_setup import *
from app.models import Category, Link, Vehicle


class LinkParser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def get_links(self, cat):
        self.driver.get("https://shop.advanceautoparts.com/")
        try:
            search_input = self.wait.until(
                EC.element_to_be_clickable((By.ID, "search-input"))
            )
            search_input.send_keys(cat.category)
            search_input.send_keys(Keys.ENTER)
        except TimeoutException:
            print("Search input not found")
            return
        for car in Vehicle.objects.filter(status="New"):
            try:
                vehicle_type_input = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "vehicleType-input"))
                )
                vehicle_type_input.send_keys(car.vehicle_type)
                vehicle_type_input.send_keys(Keys.ENTER)
            except TimeoutException:
                print("Vehicle type input not found")
                return

            try:
                vehicle_year_input = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "vehicleYear-input"))
                )
                vehicle_year_input.send_keys(car.vehicle_year)
                vehicle_year_input.send_keys(Keys.ENTER)
            except TimeoutException:
                print("Vehicle year input not found")
                return

            try:
                vehicle_make_input = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "vehicleMake-input"))
                )
                vehicle_make_input.send_keys(car.vehicle_make)
                time.sleep(1)
                vehicle_make_input.send_keys(Keys.ENTER)
            except TimeoutException:
                print("Vehicle make input not found")
                return

            try:
                vehicle_model_input = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "vehicleModel-input"))
                )
                vehicle_model_input.send_keys(car.vehicle_model)
                time.sleep(1)
                vehicle_model_input.send_keys(Keys.ENTER)
            except TimeoutException:
                print("Vehicle model input not found")
                return

            try:
                vehicle_engine_input = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "vehicleEngine-input"))
                )
                vehicle_engine_input.send_keys(car.vehicle_engine)
                vehicle_engine_input.send_keys(Keys.ENTER)
            except TimeoutException:
                print("Vehicle engine input not found")
                return

            try:
                primary_button = self.wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "primaryRedesign"))
                )
                primary_button.click()
            except TimeoutException:
                print("Primary button not found")
                return

            time.sleep(2)

            while True:
                try:
                    elements = self.wait.until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "css-195wmup"))
                    )
                except TimeoutException:
                    break

                for element in elements:
                    link_element = element.find_element(By.CLASS_NAME, "css-vurnku")
                    link_url = link_element.get_attribute("href")

                    defaults = {"category": cat.category, "vehicle_make": car.vehicle_make}

                    link, created = Link.objects.get_or_create(
                        link=link_url, defaults=defaults
                    )
                    if link.vehicle_make != car.vehicle_make:
                        link.vehicle_make += ", " + car.vehicle_make
                    link.save()

                try:
                    parent_div = self.driver.find_element(By.CLASS_NAME, "css-38ncs6")
                    target_div = parent_div.find_elements(By.CLASS_NAME, "css-vurnku")[-1]
                except NoSuchElementException:
                    break

                if not target_div.get_attribute("disabled"):
                    self.driver.execute_script("arguments[0].click();", target_div)
                else:
                    break

            try:
                self.driver.find_element(By.CLASS_NAME, "css-1d0cume").click()
                delete = self.driver.find_element(By.CLASS_NAME, "css-6cpdoq")
                delete.click()
                self.driver.find_element(By.CLASS_NAME, "destructive.css-1griu7n").click()
            except NoSuchElementException:
                pass
            car.status = "Done"
            car.save()

        cat.status = "Done"
        cat.save()

    def cleanup(self):
        self.driver.quit()


def main():
    parser = LinkParser()
    for cat in Category.objects.filter(status="New"):
        parser.get_links(cat)

    parser.cleanup()


if __name__ == "__main__":
    main()
