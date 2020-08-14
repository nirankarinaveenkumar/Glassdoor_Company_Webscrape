from selenium import webdriver
import pandas as pd
import time
import math
from bs4 import BeautifulSoup
from selenium.common import exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# Creating DataFrame
data = pd.DataFrame(columns=["Company", "Size" , "Industry"])



# Getting the URL
#url_ = input("Enter the URL ")
driver = webdriver.Chrome("/Users/Navee/bin/chromedriver")
#driver.maximize_window()

# You can input your URL here 
driver.get("https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=0&page=1&isHiringSurge=0&locId=218&locType=M&locName=Dallas-Fort%20Worth,%20TX%20Area&sector=10013")


time.sleep(2)

#Finding the number of pages so that we get the loop count.
pages_ = math.ceil(int(driver.find_element_by_xpath('.//span[@class="common__commonStyles__subtleText resultCount"]').text.split()[3])/10)
print(pages_)
current_page = 0


# Creating a function for scrolling to the next page
def go_to_next_page():
    try:
        driver.find_element_by_xpath('.//button[@aria-label="Next"]').click()
        time.sleep(2)
    except NoSuchElementException:
        return 'Fail'

    
    
for i in range(1,pages_+1):
    
    ###### Using this condition to skip the first page and after that go to the next page
    if i!=1:
        
        # Sometimes due to poor internet connection or lag the page might not load so just a check to make sure the page has loaded
        if go_to_next_page() == 'Fail':
            driver.get("https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=0&page="
                       +str(i)+
                       "&isHiringSurge=0&locId=218&locType=M&locName=Dallas-Fort%20Worth,%20TX%20Area&sector=10013")


        time.sleep(3)
    ######

    all_job = driver.find_elements_by_xpath('.//div[@class="col-md-8"]/section')
    
    
    # Looping through all the sections of companies
    for job in all_job:
        try:
            result_html = job.get_attribute('innerHTML')
        except:
            driver.refresh()
            time.sleep(2)
            result_html = job.get_attribute('innerHTML')

        
        soup = BeautifulSoup(result_html, 'html.parser')
        title = soup.find("h2").text.replace('\n','')
        size = soup.find(class_="col-lg-4 mt-sm mt-sm-std order-3").text
        industry = soup.find('span',{'data-test':'employer-industry'}).text
        print(title,size,industry)


        time.sleep(0.5)
        data = data.append({"Company": title, "Size": size , "Industry": industry}, ignore_index=True)


    print("Page "+ str(i) + " Done")


data.to_csv("louisiana_health.csv",index=False)

