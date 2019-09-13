#This is a general purpose python web scrapper

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from dbHelper import DbHelper

class MySpider():

    def __init__(self, url, enable_headless, number_of_scrolls):
        self.url = url
        self.enable_headless = enable_headless
        self.number_of_scrolls = number_of_scrolls
        self.all_items = []
        self.db = DbHelper()


    def start_driver(self):
        print("starting driver...")
        options = Options()
        if(self.enable_headless):
            options.headless = True
        self.driver = webdriver.Chrome(chrome_options=options)

    def close_driver(self):
        print("closing driver...")
        self.driver.quit()
        print("driver closed.")

    def parse_page(self):
        self.start_driver()
        self.driver.get(self.url)
        start = 0
        end = 1000
        for i in range(1, self.number_of_scrolls):
            self.driver.execute_script("window.scrollTo("+str(start)+", "+str(end)+");")
            start+=1000
            end+=1000
            sleep(5)

        self.all_items = self.driver.find_elements_by_xpath(".//*[@class='ripple movie-card vertical']")

        self.store_items()
        self.close_driver()

    def store_items(self):
        db_movies = self.db.get_movies('hotstar')

        for parent_element in self.all_items:
            name = parent_element.find_element_by_xpath(".//*[@class='content-title ellipsise']").get_attribute("innerHTML")
            image_url = parent_element.find_element_by_xpath(".//*[@class='card  card-img-container']").find_element_by_tag_name("img").get_attribute("src")
            try:
                flag_element = parent_element.find_element_by_xpath(".//*[@class='flag_element']")
            except NoSuchElementException:
                flag_element = False

            if name.strip() not in db_movies:
                self.db.addMovies(movie_name.strip(), "hotstar", play_url, image_url, is_paid)



url = "https://example.com" #url of the site you want to parse
enable_headless = True #Turning this flag to false will enable the chrome to open a new window. Tutning it will keep the code runing in virtual mode.
number_of_scrolls = 7
spider = MySpider(url, enable_headless, number_of_scrolls)
spider.parse_page()
