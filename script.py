""" filename: script.py """

import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
import csv

# function to ensure all key data fields have a value
def validate_field(field):
	# if field is present pass 
	if field:
		pass
	# if field is not present print text 
	else:
		field = 'No results'
	return field

# defining new variable passing two parameters
writer = csv.writer(open(parameters.file_name, 'w'))

# writerow() method to the write to the file object
writer.writerow(['Name', 'Job Title', 'Company', 'College', 'Location', 'URL', 'About', 'Experience'])

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://www.linkedin.com')

username = driver.find_element_by_class_name('input__input')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_id('session_password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()
sleep(0.5)

def search(query):
	driver.get('https:www.google.com')
	sleep(3)

	search_query = driver.find_element_by_name('q')
	search_query.send_keys(parameters.search_query)
	sleep(0.5)

	search_query.send_keys(Keys.RETURN)
	sleep(3)

	linkedin_urls = driver.find_elements_by_class_name('iUh30')

	return linkedin_urls


def check_urls(linkedin_urls):
	linkedin_urlz = list()
	for url in linkedin_urls:
		urls = url.text.split()
		if len(urls) == 0:
			continue
		else:
			linkedin_urlz.append(urls[2])

	return linkedin_urlz

def save(linkedin_urlz):
	for name in linkedin_urlz:

		driver.get('https://uk.linkedin.com/in/'+name)

		sleep(5)

		sel = Selector(text = driver.page_source)

		# xpath to extract the text from the class containing the name
		name = sel.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()

		if name:
			name = name.strip()

		# xpath to extract the text from the class containing the job title

		job_title = sel.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal break-words")]/text()').extract_first()

		if job_title:
			job_title = job_title.strip()

		# xpath to extract the text from the class containing the company
		company = sel.xpath('//*[starts-with(@class, "text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view")]/text()').extract_first()

		if company:
			company = company.strip()

		# xpath to extract the text from the class containing the college
		college = sel.xpath('//*[starts-with(@id, "ember97")]/text()').extract_first()

		if college:
			college = college.strip()

		# xpath to extract the text from the class containing the location

		location = sel.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()

		if location:
			location = location.strip()

		about = sel.xpath('//*[starts-with(@class, "lt-line-clamp__line")]/text()').extract_first()

		if about:
			about = about.strip()

		exp = sel.xpath('//*[starts-with(@class, "t-16 t-black t-bold")]/text()').extract_first()

		if exp:
			exp = exp.strip()

		linkedin_url = driver.current_url

		# validating if the fields exist on the profile
		name = validate_field(name)
		job_title = validate_field(job_title)
		company = validate_field(company)
		college = validate_field(college)
		location = validate_field(location)
		linkedin_url = validate_field(linkedin_url)
		about = validate_field(about)
		exp = validate_field(exp)

		# writing the corresponding values to the header
		writer.writerow([name.encode('utf-8'),
                 job_title.encode('utf-8'),
                 company.encode('utf-8'),
                 college.encode('utf-8'),
                 location.encode('utf-8'),
                 linkedin_url.encode('utf-8'),
                 about.encode('utf-8'),
                 exp.encode('utf-8')])

for search_query in ['site:linkedin.com/in/ AND "python developer"', 'site:linkedin.com/in/ AND "data scientist"']:
	
	linkedin_urls = search(search_query)

	#linkedin_urls = [url.text.split()[2] for url in linkedin_urls]
	linkedin_urlz = check_urls(linkedin_urls)

	sleep(0.5)

	save(linkedin_urlz)

driver.quit()