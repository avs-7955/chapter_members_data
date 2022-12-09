from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Website containing data about the Chapter Members
website = 'https://bni-india.in/en-IN/chapterdetail?chapterId=P%2BIWaeuOSfF3Mxm03FLSzA%3D%3D&name=BNI+BNI+Alpha'

# Chrome Driver path
driver = webdriver.Chrome("D:\VIT\Self_Dev\CODING\Web Scraping\chromedriver")

driver.get(website)
time.sleep(5)  # Wating for the website to be fetched

# Clicking the all members btn
members_btn = driver.find_element(By.XPATH, '//a[@class="numberLink"]')
driver.execute_script("arguments[0].click();", members_btn)

page_source = driver.page_source

# Integrating BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Creating empty list for the data
name = []
company = []
prof = []
phone = []
profile_url = []


def extract_data():
    # Finding the rows of the table
    members_list = soup.find_all('tr', attrs={'role': 'row'})
    # Extracing the information and appending it to the lists
    for member in members_list:
        text = member.text.strip()
        arr = text.split('\n')
        if(len(arr) != 1):
            name.append(arr[0])
            company.append(arr[1])
            prof.append(arr[2])
            # If the phone number isn't available, adding blank string
            if(len(arr) <= 3):
                phone.append(' ')
            else:
                phone.append(arr[3])
    # Extracing profile URL of all the members
    all_links = soup.findAll('a', class_='linkone')
    for link in all_links:
        if(len(link['href']) != 0):
            profile_url.append(f"https://bni-india.in/en-IN/{link['href']}")
        else:
            profile_url.append(' ')


extract_data()
time.sleep(5)

# Clicking the button to get the next page elements
click_nxt_btn = driver.find_element(
    By.XPATH, '//li[@class="paginate_button next"]')
driver.execute_script("arguments[0].click();", click_nxt_btn)

# Integrating BeautifulSoup and extracting data
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
extract_data()
time.sleep(5)

# Clicking the button to get the next page elements
click_nxt_btn = driver.find_element(
    By.XPATH, '//li[@class="paginate_button next"]')
driver.execute_script("arguments[0].click();", click_nxt_btn)

# Integrating BeautifulSoup and extracting data
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
extract_data()

# Creating a data frame and stroring the data into excel file
df = pd.DataFrame({'MemberName': name, 'Company': company,
                   'Profession': prof, 'MobileNo.': phone, 'ProfileURL': profile_url})
df.to_excel('members_list.xlsx', index=False)
