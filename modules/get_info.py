from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django_setup import *
from app.models import Link, ProductInfo


class InfoParser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def get_info(self, link_obj):
        self.driver.get(link_obj.link)

        try:
            title_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-99vq1c")))
            title = title_element.text.strip()
        except NoSuchElementException:
            title = None

        try:
            reviews_element = self.driver.find_element(By.CLASS_NAME, "css-1eymw9y")
            reviews = reviews_element.get_attribute("aria-label").strip()
        except NoSuchElementException:
            reviews = None

        try:
            count_of_reviews_element = self.driver.find_element(By.CLASS_NAME, "css-1u1rtir")
            count_of_reviews = count_of_reviews_element.text.strip()
        except NoSuchElementException:
            count_of_reviews = None

        try:
            part_element = self.driver.find_element(By.CLASS_NAME, "css-tvrt7a")
            part = part_element.text.strip()
        except NoSuchElementException:
            part = None

        try:
            price_element = self.driver.find_element(By.CLASS_NAME, "css-yqosfv")
            price = price_element.get_attribute("aria-label").strip()
        except NoSuchElementException:
            price = None

        try:
            product_details_element = self.driver.find_element(By.ID, "product-details-d")
            product_details = product_details_element.text.strip()
        except NoSuchElementException:
            product_details = None

        try:
            specifications_element = self.driver.find_element(By.ID, "product-specifications")
            specifications = specifications_element.text.strip()
        except NoSuchElementException:
            specifications = None

        ProductInfo.objects.create(
            link=link_obj.link,
            title=title,
            reviews=reviews,
            count_of_reviews=count_of_reviews,
            part=part,
            price=price,
            product_details=product_details,
            specifications=specifications,
            category=link_obj.category,
            vehicle_make=link_obj.vehicle_make
        )

        link_obj.status = "Done"
        link_obj.save()

    def cleanup(self):
        self.driver.quit()


def main():
    parser = InfoParser()
    for link in Link.objects.filter(status="New"):
        parser.get_info(link)

    parser.cleanup()


if __name__ == '__main__':
    main()
