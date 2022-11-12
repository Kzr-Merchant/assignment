import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions  as EC
from  selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from  selenium.webdriver.common.action_chains import ActionChains



srv = Service("C:\\webdrivers\\chromedriver.exe")
driver = webdriver.Chrome(service=srv) # This is to surpass warning given by Selenium
wait = WebDriverWait(driver,30)
driver.maximize_window()


def validate_price_range(min,max,prices):
    '''
        Function used to compare price range displayed on the page , between given min & max range
    '''
    for price  in prices:
        driver.execute_script('arguments[0].scrollIntoView()',price)
        formated_price = int(price.text.replace(',','')) # removing comma(,) in numbers to make in Base10 for comparing
        assert formated_price in range(min,max)




############# step 1 # searching Amazon in Google #############################
driver.get('https://www.google.com/search?q=amazon')
############# step 2 # printing all search result in Google #############################
searched_link = driver.find_elements(By.XPATH,'.//div/a/h3') # xpath for all searched elements in browser window

for link in searched_link:
    print(link.text) # printing all search result texts
############# step 5. Click on the link which takes you to the amazon login page. #############################
Amazon_link = driver.find_element(By.XPATH,'.//h3[contains(text(),\'Amazon.in\')]').click() # clicking link containing 'Amazon.in'
############# step 6. login to https://www.amazon.in/ #############################

signin_link = driver.find_element(By.XPATH,'.//span[@id=\'nav-link-accountList-nav-line-1\']')

act = ActionChains(driver)

wait.until(EC.visibility_of_element_located((By.XPATH,'.//span[@id=\'nav-link-accountList-nav-line-1\']')))
act.move_to_element(signin_link)
signin_link.click()

email_id_text = driver.find_element(By.ID,'ap_email').send_keys('user_nanme') # please provide a valid username
continue_but = driver.find_element(By.ID,'continue').click()
password_text = driver.find_element(By.ID,'ap_password').send_keys('password') # provide a password for above user
signin_continue = driver.find_element(By.ID,'signInSubmit').click()

############# step 7. click on all buttons on search & select Electronics. #############################

search_dd = driver.find_element(By.XPATH,'.//select[@id=\'searchDropdownBox\']') #Search drop down
catogary_dd = Select(driver.find_element(By.XPATH,'.//select[@id=\'searchDropdownBox\']'))
search_dd.click()
wait.until(EC.visibility_of_all_elements_located((By.XPATH,'.//select[@id=\'searchDropdownBox\']//option'))) # waiting to load all available options
catogary_dd_options = driver.find_elements(By.XPATH,'.//select[@id=\'searchDropdownBox\']//option') # getting list of all available options

for i in catogary_dd_options:
    catogary_dd.select_by_visible_text(i.text) # selecting all option using its text
catogary_dd.select_by_visible_text('Electronics') # select 'Electronic' option
driver.find_element(By.ID,'twotabsearchtextbox').send_keys('Dell computers')
driver.find_element(By.ID,'nav-search-submit-button').click()

############# 9. apply the filter of range Rs 20000 to 30000  #############################
min_XPATH = ".//input[@id=\'low-price\']"
Max_XPATH =".//input[@id=\'high-price\']"
Go_XPATH = ".//input[@class=\'a-button-input\']"
min_text_field = driver.find_element(By.XPATH,min_XPATH)
max_text_field = driver.find_element(By.XPATH,Max_XPATH)
Go_but = driver.find_element(By.XPATH,Go_XPATH)
five_out_of_five = driver.find_element(By.XPATH,'.//span[contains(text(),\'5 out of 5\')]')

driver.execute_script('arguments[0].scrollIntoView()',min_text_field) # scrolling page to get min/max input field in viewable area
min_text_field.send_keys(20000)
max_text_field.send_keys(30000)
Go_but.click()


############# 10. Validate all the products on the first 2 pages are shown in the range of Rs 30000 to 50000 #############################
driver.execute_script('arguments[0].scrollIntoView()',driver.find_element(By.XPATH,min_XPATH))
driver.find_element(By.XPATH,min_XPATH).send_keys(30000)
driver.find_element(By.XPATH,Max_XPATH).send_keys(50000)
driver.find_element(By.XPATH,Go_XPATH).click()
Xpath_for_price = './/span[contains(@class,\'a-price-whole\')]' # xpath for price tag displayed for items
item_prices = driver.find_elements(By.XPATH,Xpath_for_price) # getting all prices
validate_price_range(30000,50000,item_prices) # function to assert & validate if price listed in the page is within the given range or not!


next_but_xpath = './/a[contains(@class,\'pagination-next\')]' # xpath for Next button (by default we are on 1st page )
next_page_button = driver.find_element(By.XPATH,next_but_xpath)
wait.until(EC.visibility_of_element_located((By.XPATH,'.//a[contains(@class,\'s-pagination-next\')]'))) # waiting till page is fully loaded(Next button is visible)
next_page_button.click() # moving to second_page


item_prices = driver.find_elements(By.XPATH,Xpath_for_price)
validate_price_range(30000,50000,item_prices) # function to assert & validate if price listed in the page is within the given range or not!
driver.back() # moving to first page again!!
############# 11. print all the products on the first 2 pages whose rating is 5 out of 5 #############################
# five_rating_products_xpath = './/i[contains(@class,\'a-star-small-5\')]'
wait.until(EC.visibility_of_element_located((By.XPATH,next_but_xpath))) # wait till page is fully loaded!
five_rating_products_xpath = './/span[contains(text(),\'5.0 out of 5 stars\')]//preceding::div[1]//h2/a/span'
five_rating_products = driver.find_elements(By.XPATH,five_rating_products_xpath)
for product in five_rating_products:
    print(product.text)
driver.find_element(By.XPATH,next_but_xpath).click() # moving to second_page
wait.until(EC.visibility_of_element_located((By.XPATH,'.//a[contains(@class,\'s-pagination-next\')]'))) # waiting till page is fully loaded(Next button is visible)
five_rating_products = driver.find_elements(By.XPATH,five_rating_products_xpath)
for product in five_rating_products:
    print(product.text) # printing 5 rating products displayed on second page!


############# 12. add the first product whose rating is 5 out of 5 to the wish list. (Create a new wish list) #############################
driver.execute_script('arguments[0].scrollIntoView()',five_rating_products[0]) # scrolling page to 1st 5rating item
five_rating_products[0].click() # selecting 1st item with 5 rating

############# 12. add the first product whose rating is 5 out of 5 to the wish list. (Create a new wish list) #############################
add_to_withlist_btn_xpath  = './/input[@id=\'add-to-wishlist-button-submit\']'
add_to_wishlist_btn = driver.find_element(By.XPATH,add_to_withlist_btn_xpath)
add_to_wishlist_btn.click()
