from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

s_count=0
f_count=0

page_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1" 
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(page_url)

full_data=[]

page_number=1
while(page_number<=20):

    filtered_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 's-title-instructions-style')]/..")
    
    for card in filtered_cards:
        # Extract product details
        try:
            product_url = card.find_element(By.XPATH, ".//h2/a").get_attribute('href')
            product_name = card.find_element(By.XPATH, './/h2//span').text 
            product_prices=card.find_elements(By.XPATH, ".//span[contains(@class, 'price-whole')]")
            product_rating = card.find_element(By.XPATH, ".//span[contains(text(), 'out of')]").get_attribute('textContent')
            product_reviews = card.find_element(By.XPATH, ".//span[contains(text(), 'out of')]/../../../../../span[2]").text
                 
            # Print product details
            print("Product URL:", product_url)
            print("Product Name:", product_name)
            print("Rating:", product_rating)
            prices=[]
            for price in product_prices:
                print("Price:",price.text)
                prices.append(price.text)
            print("Number of Reviews:", product_reviews)
            print("---")
            s_count+=1

            #Store in CSV File
            data=(product_url,product_name,prices,product_rating,product_reviews)
            full_data.append(data)
        except:
            print("Not Found")
            f_count+=1

    next_page_link=driver.find_element(By.XPATH, "//span[contains(@class, 's-pagination-strip')]/a[contains(text(), 'Next')]")
    next_page_link.click()
    time.sleep()
    page_number+=1

with open('part1.csv','w',newline='',encoding='utf-8') as f:
    header=['URL','NAME','PRICES','RATING','REVIEWS']
    writer=csv.writer(f)
    writer.writerow(header)
    writer.writerows(full_data)

print(s_count)
print(f_count)

driver.quit()
