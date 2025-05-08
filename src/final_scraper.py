from collections import namedtuple
import re
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeService, ChromeOptions, Chrome
from selenium.common.exceptions import WebDriverException
import time
import sys
from csv import writer
import logging
from dotenv import load_dotenv
from os import getenv


RealtorData = namedtuple(
    "RealtorData", ["name", "role", "company", "address", "number"]
)

BATCH_SIZE = 8
DEFAULT_PAGES_TO_SCRAPE = 1
DEFAULT_FILENAME = "realtor_data"

LOGGER = logging.getLogger("scraper")
LOGGER.setLevel(logging.DEBUG)

STD_OUT_LOGGER = logging.StreamHandler(sys.stdout)
STD_OUT_LOGGER.setLevel(logging.DEBUG)

LOGGER.addHandler(STD_OUT_LOGGER)

load_dotenv()
URL = getenv("WEBSITE_URL")
assert isinstance(URL, str)


def provision_webdriver():
    try:
        service = ChromeService()
        options = ChromeOptions()
        options.add_argument("--enable-javascript")
        driver = Chrome(service=service, options=options)
        LOGGER.info(f"Created driver: {driver}")

    except WebDriverException as e:
        LOGGER.critical(f"Something went wrong with Webdriver setup: {e}")
        sys.exit()

    return driver


def sanitize(input_str):
    return " ".join(input_str.split())


# TODO: Should force directory to be in a folder
# called output in top level dir of project
def initialize_csv(input_name):
    try:
        filename = f"{input_name}.csv"
        with open(filename, "w") as file:
            csv_writer = writer(file)
            csv_writer.writerow(list(RealtorData._fields))
    except (FileNotFoundError, PermissionError, IOError, Exception) as e:
        LOGGER.critical(f"Can't write to file: {e}")
        sys.exit()
    return filename


def write_to_csv(filename, pages_data):
    try:
        with open(filename, "a") as file:
            csv_writer = writer(file)
            for page in pages_data:
                csv_writer.writerows(page)
    except (FileNotFoundError, PermissionError, IOError, Exception) as e:
        LOGGER.critical(f"Can't write to file: {e}")
        sys.exit()
    return filename


def check_input_pages(input_pages):
    if input_pages.isdigit() and int(input_pages) > 0:
        pages_to_scrape = int(input_pages)
    else:
        LOGGER.error("Seems like you entered an invalid number")
        LOGGER.error("We'll set input pages to 1")
        pages_to_scrape = DEFAULT_PAGES_TO_SCRAPE
    return pages_to_scrape


def check_input_filename(input):
    properfilename = re.compile("^[a-zA-Z0-9_.-]*$")
    if properfilename.match(input):
        filename = input
    else:
        LOGGER.error(
            "Seems like you entered an invalid file name that is not in the set [0-9a-zA-Z-_]"
        )
        LOGGER.error(f"We're going to set the filename to: {DEFAULT_FILENAME}.csv")
        filename = DEFAULT_FILENAME
    return filename


def collect_realtor_data_from_page(soup):
    realtor_card_divs = soup.find_all(id=re.compile("RealtorCard-[0-9]*"))
    assert len(realtor_card_divs) != 0

    page_data = []

    for card in realtor_card_divs:
        try:
            name = card.find(class_="realtorCardName").text
            realtor_name = sanitize(name)
        except (TypeError, AttributeError):
            realtor_name = ""
            LOGGER.error(f"Could not get name for {card}")

        try:
            role = card.find(class_="realtorCardTitle").text
            realtor_role = sanitize(role)
        except (TypeError, AttributeError):
            realtor_role = ""
            LOGGER.error(f"Could not get role for {card}")

        try:
            company = card.find(class_="realtorCardOfficeName").text
            realtor_company = sanitize(company)
        except (TypeError, AttributeError):
            realtor_company = ""
            LOGGER.error(f"Could not get company for {card}")

        try:
            address = card.find(class_="realtorCardOfficeAddress").text
            realtor_address = sanitize(address)
        except (TypeError, AttributeError):
            realtor_address = ""
            LOGGER.error(f"Could not get address for {card}")

        try:
            number = card.find(class_="realtorCardContactNumber TelephoneNumber").text
            realtor_number = sanitize(number)
        except (TypeError, AttributeError):
            realtor_number = ""
            LOGGER.error(f"Could not get number for {card}")

        realtor_data = RealtorData(
            name=realtor_name,
            role=realtor_role,
            company=realtor_company,
            address=realtor_address,
            number=realtor_number,
        )

        page_data.append(realtor_data)

    return page_data


def render_page(driver, url):
    try:
        driver.get(url)
        # Wait for webpage to load, may need to change this depending
        # On internet speed and hardware specs, this is also because the site is loading in JS and .get() above will not catch that
        time.sleep(8)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except (WebDriverException, Exception) as e:
        LOGGER.error(f"Could not load page, more info {e}")
        raise e

    page_data = collect_realtor_data_from_page(soup)
    return page_data


def scrape_pages(driver, filename, pages_to_scrape=DEFAULT_PAGES_TO_SCRAPE):
    for batch_start in range(1, pages_to_scrape + 1, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, pages_to_scrape + 1)
        data_from_pages = []

        for page_num in range(batch_start, batch_end):
            url = URL + str(page_num)
            LOGGER.info(f"Rendering url: {url}")

            page_data = render_page(driver, url)
            data_from_pages.append(page_data)

        LOGGER.info(f"Writing batch for pages {batch_start} to {batch_end - 1}")
        write_to_csv(filename, data_from_pages)
        LOGGER.info("Wrote batch above to CSV")



def main():
    if len(sys.argv) == 3:
        pages_to_scrape = check_input_pages(sys.argv[1])
        filename = check_input_filename(sys.argv[2])

    if len(sys.argv) == 2:
        pages_to_scrape = check_input_pages(sys.argv[1])
        filename = DEFAULT_FILENAME

    if len(sys.argv) == 1:
        pages_to_scrape = DEFAULT_PAGES_TO_SCRAPE
        filename = DEFAULT_FILENAME

    if len(sys.argv) > 3:
        LOGGER.critical(
            "Looks like more than 3 arguments were supplied.\
            The first is number of pages to scrape, \
            second argument should be the name of the file you want to save to e.g myfile, data_file"
        )
        sys.exit()

    LOGGER.info(f"pages input: {pages_to_scrape} filename: {filename}")

    driver = provision_webdriver()
    filename = initialize_csv(filename)
    scrape_pages(driver, filename, pages_to_scrape)
    driver.quit()


if __name__ == "__main__":
    main()
