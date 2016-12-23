from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


path_to_chromedriver = 'C:/Users/Suggu/Downloads/chromedriver_win32/chromedriver'
yellowpages_boats = []
list_of_states = ['AL','AK']
for state in list_of_states:
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)
	url = 'http://www.yellowpages.com/search?search_terms=Boat+Dealers&geo_location_terms=%s'%state
	browser.get(url)
	assert "Boat Dealers" in browser.title
	no_of_pages = browser.find_element_by_css_selector("div.pagination p").text
	pages = no_of_pages.split(' ')
	total_count = pages[2].replace("results","")
	total_count = int(total_count)
	num_pages = total_count//30
	#print num_pages
	pages_range = range(1,num_pages+1)
	browser.close()
	# Dynamically taking state value as key here
	for page in pages_range:
		browser = webdriver.Chrome(executable_path = path_to_chromedriver)
		url = 'http://www.yellowpages.com/search?search_terms=Boat+Dealers&geo_location_terms=%s&page=%d'%(state,page)
		browser.get(url)
		result_divs = browser.find_elements_by_css_selector('div.result div.srp-listing div.v-card div.info')
		#print result_divs
		for result_div in result_divs:
			try:
				boat_name = result_div.find_element_by_css_selector("h3.n").text
			except:
				boat_name = "NA"
			try:
				address1 = result_div.find_element_by_css_selector("div.info-primary p.adr span.street-address").text
			except:
				address1 = "NA"
			try:
				website = result_div.find_element_by_css_selector("div.info-secondary div.links a").get_attribute('href')
			except:
				website = "NA"
			try:
				address2= result_div.find_element_by_css_selector("div.info-primary p.adr span.locality").text
			except:
				address2 = "NA"
			try:
				city=result_div.find_element_by_css_selector("div.info-primary p.adr span:nth-child(3)").text
			except:
				city = "NA"
			try:
				Zipcode=result_div.find_element_by_css_selector("div.info-primary p.adr span:nth-child(4)").text
			except:
				Zipcode="NA"
			try:
				Phonenumber=result_div.find_element_by_css_selector("div.info-primary div.phones").text
			except:
				Phonenumber="NA"
			yellowpages_boats.append({'Boat Name':boat_name,'Address 1':address1,'Website':website, 'Address 2':address2, 'City': city, 'Zipcode':Zipcode, 'Phonenumber':Phonenumber})
		browser.close()
		#print yellowpages_boats

print (pd.DataFrame(yellowpages_boats))
df = pd.DataFrame(yellowpages_boats)
df.to_csv('boatdealers.csv', index=False, encoding="UTF-8")
