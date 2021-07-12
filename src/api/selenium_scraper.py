import time, sys
from bs4 import BeautifulSoup
from selenium import webdriver
from stop_words import stop_words
from mongo import add_item, delete_collection
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class Scraper:

    def __init__(self):
        self.chrome_options = Options()

        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument(" --disable-web-security")

        # self.b = webdriver.Chrome(options=self.chrome_options, executable_path="/Users/jackowens/Documents/status-dashboard/chromedriver")
        self.b = webdriver.Chrome(options=self.chrome_options)
        self.stop_words = stop_words.get("general")


    def run_auction_search (self, search_term: str, min_price: str, max_price: str):
        """Run eBay auction search query with search filters and price constraints."""

        self.b.get("https://www.ebay.com/sch/ebayadvsearch")
        self.b.implicitly_wait(2)

        self.search_query = self.b.find_element_by_xpath("//*[@id='_nkw']")
        self.search_query.click()
        self.search_query.send_keys(search_term + self.stop_words)

        self.auction = self.b.find_element_by_xpath("//*[@id='LH_Auction']")
        self.auction.click()

        self.condition_used = self.b.find_element_by_xpath("//*[@id='LH_ItemConditionUsed']")
        self.condition_used.click()

        self.condition_unspecified = self.b.find_element_by_xpath("//*[@id='LH_ItemConditionNS']")
        self.condition_unspecified.click()

        self.number_of_bids_checkbox = self.b.find_element_by_xpath("//*[@id='LH_NOB']")
        self.number_of_bids_checkbox.click()
        self.min_bids = self.b.find_element_by_xpath("//*[@id='_sabdlo']")
        self.min_bids.send_keys(Keys.NUMPAD1)
        self.max_bids = self.b.find_element_by_xpath("//*[@id='_sabdhi']")
        self.max_bids.send_keys(Keys.NUMPAD9)
        self.max_bids.send_keys(Keys.NUMPAD9)

        self.search_button = self.b.find_element_by_xpath("//*[@id='searchBtnLowerLnk']")
        self.search_button.click() # click search button

        self.b.get(self.b.current_url + f"&_udhi={max_price}&rt=nc&_udlo={min_price}") # set min/max price
        self.b.get(self.b.current_url + "&_sop=1") # sort by ending soonest

        # Save Page Source
        page_source_results = self.b.page_source
        soup = BeautifulSoup(page_source_results, features="lxml")

        # Parse Item Titles
        listings = soup.find_all("li", class_="sresult") # <class 'bs4.element.ResultSet'>

        # Loops through all listings and adds DB properties to lists
        item_titles, item_prices, item_bids, time_remaining, item_urls = [], [], [], [], []
        for listing in listings:
            _item = " " # Removes "New Listing" prefix

            price = listing.find('span', attrs={'class':"bold"}) or None
            if price is not None:
                item_prices.append(price.text)

            title = listing.find('h3', attrs={'class':"lvtitle"}) or None
            if title is not None:
                item_titles.append(title.text)

            bids = listing.find('li', attrs={'class':"lvformat"}) or None
            if bids is not None:
                item_bids.append(bids.text)

            for elem in listing.find_all('span', attrs={'class':"HOURS"}):
                for items in elem:
                    try:
                        time_remaining.append(items.partition('\n')[0])
                    except TypeError:
                        time_remaining.append("")

            for item in listing.find_all('a', attrs={'class':"vip"}):
                item_urls.append(item["href"])

        # print(item_prices, file=sys.stderr)
        # print(item_titles, file=sys.stderr)
        # print(item_bids, file=sys.stderr)
        # print(time_remaining, file=sys.stderr)
        # print(item_urls, file=sys.stderr)

        delete_collection(search_term)
        for title, price, bids, urls, remaining in zip(item_titles, item_prices, item_bids, item_urls, time_remaining):
            add_item(title, price, bids, urls, remaining, collection_name=search_term)

        self.b.quit()


    def run_bit_search (self, search_term: str, min_price: str, max_price: str):
        """Run eBay buy it now search query with search filters and price constraints."""

        self.b.get("https://www.ebay.com/sch/ebayadvsearch")
        self.b.implicitly_wait(2)

        self.search_query = self.b.find_element_by_xpath("//*[@id='_nkw']")
        self.search_query.click()
        self.search_query.send_keys(search_term + self.stop_words)

        self.buy_it_now = self.b.find_element_by_xpath("//*[@id='LH_BIN']")
        self.buy_it_now.click()

        self.condition_used = self.b.find_element_by_xpath("//*[@id='LH_ItemConditionUsed']")
        self.condition_used.click()

        self.condition_unspecified = self.b.find_element_by_xpath("//*[@id='LH_ItemConditionNS']")
        self.condition_unspecified.click()

        self.started_within_checkbox = self.b.find_element_by_xpath("//*[@id='LH_Time']")
        self.started_within_checkbox.click()

        self.b.find_element_by_xpath("//select[@name='_ftrt']/option[text()='Started within']").click() # specify started within
        self.b.find_element_by_xpath("//select[@name='_ftrv']/option[text()='5 hours']").click() # specify 5 hours

        self.search_button = self.b.find_element_by_xpath("//*[@id='searchBtnLowerLnk']")
        self.search_button.click() # click search button

        self.b.get(self.b.current_url + f"&_udhi={max_price}&rt=nc&_udlo={min_price}") # set min/max price
        self.b.get(self.b.current_url + "&_sop=10") # sort by newly listed

        # Save Page Source
        page_source_results = self.b.page_source
        soup = BeautifulSoup(page_source_results, features="lxml")

        # Parse Item Titles
        listings = soup.find_all("li", class_="sresult") # <class 'bs4.element.ResultSet'>

        # Loops through all listings and adds DB properties to lists
        item_titles, item_prices, time_remaining, item_urls = [], [], [], []
        for listing in listings:
            _item = " " # Removes "New Listing" prefix

            price = listing.find('span', attrs={'class':"bold"}) or None
            if price is not None:
                item_prices.append(price.text)

            title = listing.find('h3', attrs={'class':"lvtitle"}) or None
            if title is not None:
                item_titles.append(title.text)

            for elem in listing.find_all('span', attrs={'class':"HOURS"}):
                for items in elem:
                    try:
                        time_remaining.append(items.partition('\n')[0])
                    except TypeError:
                        time_remaining.append("")

            for item in listing.find_all('a', attrs={'class':"vip"}):
                item_urls.append(item["href"])

        print(item_prices, file=sys.stderr)
        print(item_titles, file=sys.stderr)
        print(time_remaining, file=sys.stderr)
        print(item_urls, file=sys.stderr)

        delete_collection(search_term)
        for title, price, urls, remaining in zip(item_titles, item_prices, item_urls, time_remaining):
            add_item(title, price, urls, remaining, collection_name=search_term, is_auction=False)

        self.b.quit()


# Scraper().run_auction_search("sinn", "500", "7500")
# Scraper().run_bit_search("zenith", "1200", "7500")


# run_search("breguet", "4000", "17650")
