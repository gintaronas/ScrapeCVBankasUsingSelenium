import time
import re
import math
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as drWait

# Initialise the driver for Chrome
op = webdriver.ChromeOptions()
op.add_argument("--enable-javascript")
ch_driver = webdriver.Chrome(service=ChService('.\\.venv\\driver\\chromedriver.exe'), options=op)

# Opening the main page of cvbankas.lt, setting location to Vilnius -- location can be implemented differently
ch_driver.get("https://www.cvbankas.lt/?location%5B%5D=606")   # Location is set to Vilnius


# Get rid of cookies dialog by pressing "Sutinku" button
sel = "body > div.fc-consent-root > div.fc-dialog-container > div.fc-dialog.fc-choice-dialog > \
        div.fc-footer-buttons-container > div.fc-footer-buttons > button.fc-button.fc-cta-consent.fc-primary-button"
drWait(ch_driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, sel)))
sutinku_button = ch_driver.find_element(By.CSS_SELECTOR, sel)
sutinku_button.click()

# ch_driver.maximize_window()
# ch_driver.minimize_window()

# Let's make the filter for position with user input
position = input("Ko ieškome? Įveskite pareigybę: ")
sel = '//*[@id="filter_keyword"]'
initial_filter_field = ch_driver.find_element(By.XPATH, sel)
initial_filter_field.send_keys(position)   # This one we can make dynamic user input
initial_filter_field.send_keys(Keys.ENTER)
drWait(ch_driver, 3)
time.sleep(2)

# Web page is ready, let's collect needed information
sel = 'filter_statistics'
total_count_text = ch_driver.find_element(By.CLASS_NAME, sel).text
adv_found_count = re.findall('\\d+', total_count_text)
print(f'Total advertisements found: {adv_found_count[0]}')

# As we know, page contains max 50 vacancies. Let's check, how many pages of results we have
if int(adv_found_count[0]) <= 50:
    num_pages = 1
    max_search = int(adv_found_count[0]) + 1
    last_page_adv_num = int(adv_found_count[0])
    curr_page_url = ch_driver.find_element(By.XPATH, '/html/head/link[2]').get_attribute('href')
else:
    max_search = 51
    num_pages = math.ceil(int(adv_found_count[0]) / 50)
    last_page_adv_num = int((int(adv_found_count[0]) / 50) % 1 * 50)
    sel_current_page = '/html/body/div[1]/div/div/main/ul/li[1]/ul/li[1]/a'
    curr_page_url = ch_driver.find_element(By.XPATH, sel_current_page).get_attribute('href')

print(f'Number of advertisements on the last page: {last_page_adv_num}')
print(f'Total number of returned pages : {num_pages}')
print(f'Current page URL: {curr_page_url}')

input("Please press Enter to continue!")


def scrape_the_page(max_search):
    for i in range(1, max_search):
        sel_first_part = '/html/body/div[1]/div/div/main/div/article['
        sel_vacancy_name = sel_first_part + str(i) + ']/a/div[2]/div[1]/h3'
        sel_vacancy_link = sel_first_part + str(i) + ']/a'
        sel_company_name = sel_first_part + str(i) + ']/a/div[2]/div[1]/span/span'
        sel_salary_range = sel_first_part + str(i) + ']/a/div[2]/div[2]/span/span/span/span[1]/span[1]'
        sel_salary_cur = sel_first_part + str(i) + ']/a/div[2]/div[2]/span/span/span/span[1]/span[2]'
        sel_salary_tax = sel_first_part + str(i) + ']/a/div[2]/div[2]/span/span/span/span[2]'

        vacancy = ch_driver.find_element(By.XPATH, sel_vacancy_name).text
        drWait(ch_driver, 1)
        vacancy_link = ch_driver.find_element(By.XPATH, sel_vacancy_link).get_attribute('href')
        drWait(ch_driver, 1)
        company_name = ch_driver.find_element(By.XPATH, sel_company_name).text
        drWait(ch_driver, 1)

        try:  # sometimes salaries are missing, need to handle exception
            salary_range = ch_driver.find_element(By.XPATH, sel_salary_range).text
            drWait(ch_driver, 1)
            salary_cur = ch_driver.find_element(By.XPATH, sel_salary_cur).text
            drWait(ch_driver, 1)
            salary_tax = ch_driver.find_element(By.XPATH, sel_salary_tax).text
        except:
            salary_range = "n/a"
            salary_cur = "n/a"
            salary_tax = "n/a"

        # Here we define the output
        print(f'Nr. {i}, {vacancy}, {company_name}, {salary_range} {salary_cur}, {salary_tax}, Daugiau: {vacancy_link}')
        results.append((vacancy, company_name, salary_range, salary_cur, salary_tax, vacancy_link))
        i += 1


results = []
scrape_the_page(max_search)  # calling function for the first page

# input("Finished with this page, press Enter to go to the next")

# Let's scrape the remaining pages
if num_pages > 1:
    for page in range(2, num_pages + 1):
        if page == num_pages:
            max_search = last_page_adv_num + 1
        # Open the next page
        url_to_open = curr_page_url + '&page=' + str(page)
        ch_driver.get(url_to_open)
        drWait(ch_driver, 3)
        scrape_the_page(max_search)
        page += 1

# Let's write to csv file
with open('scraping_results.csv', 'w', newline='', encoding='UTF-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Vacancy', 'Company', 'Salary range', 'Curr', 'Brutto/netto', 'Link'])
    for result in results:
        writer.writerow(result)

input("Finished, press Enter to exit!")
ch_driver.close()
