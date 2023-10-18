import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()
f_count=0

# Open the CSV file containing the links
with open('part6.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row if present
    
    # Open the output CSV file to store the scraped data
    with open('part7.csv', 'w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(['Link', 'Description','ASIN','Product Description','Manufacturer'])  # Write the header row
        
        # Iterate over the links in the CSV file
        for row in reader:
            link = row[0]  #link is in the first column
            
            try:
                # Open the link in the browser
                driver.get(link)
                f_desc=[]
                p_desc=[]
                try:
                    full_description = driver.find_elements(By.XPATH, "//div[@id='feature-bullets']/ul/li")
                    asin= driver.find_element(By.XPATH, "//span[contains(text(), 'ASIN')]/../span[2]").text
                    product_desc = driver.find_elements(By.XPATH, "//div[contains(@class, 'detail-bullets-wrapper ')]//ul/li/span/span")
                    manufacturer= driver.find_element(By.XPATH, "//span[contains(text(), 'Manufacturer')]/../span[2]").text
                    
                    print(asin)
                    for description in full_description:
                        print(description.text)
                        f_desc.append(description.text)

                    for description in product_desc:
                        print(description.text)
                        p_desc.append(description.text)
                    print(manufacturer)

                except:
                    f_count+=1
                
                # Write the link and scraped data to the output CSV file
                writer.writerow([link,f_desc,asin,p_desc,manufacturer])
                
            except NoSuchElementException:
                print(f"Link not found or element not visible: {link}")
            
            except Exception as e:
                print(f"Error occurred for link {link}: {str(e)}")
        
# Close the browser and quit the driver
driver.quit()
