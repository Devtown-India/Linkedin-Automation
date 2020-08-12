""" filename: script.py """

import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
import csv
import time
import pickle


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
writer.writerow(['Name', 'Headline', 'Location', 'Headings', 'Highlights', 'Summary', 'Activity', 'Education', 'Skills', 'Interests', 'URL'])

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

with open('connections.pkl', 'rb') as f:
	mynewlist = pickle.load(f)

def save(linkedin_urlz):
	for name in linkedin_urlz:

		driver.get(name)

		sleep(5)

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

		sleep(1.5)

		sel = Selector(text = driver.page_source)

		# xpath to extract the text from the class containing the name
		name = sel.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()

		if name:
			name = name.strip()

		# xpath to extract the text from the class containing the job title

		headline = sel.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal break-words")]/text()').extract_first()

		if headline:
			headline = headline.strip()

		location = sel.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()

		if location:
			location = location.strip()

		headings = driver.find_elements_by_class_name('pv-profile-section__card-heading')
		headings = [x.text for x in headings]
		headings = ''.join(headings)		

		highlights = driver.find_elements_by_xpath("//ul[starts-with(@class,'pv-highlights-section__list list-style-none')]")
		highlights = [x.text for x in highlights]
		highlights = ''.join(highlights)		

		summary = sel.xpath('//*[starts-with(@class, "lt-line-clamp__line")]/text()').extract_first()

		if summary:
			summary = summary.strip()

		activity = driver.find_elements_by_xpath("//section[starts-with(@class,'pv-profile-section pv-recent-activity-section-v2 artdeco-container-card artdeco-card ember-view')]")
		activity = [x.text for x in activity]
		activity = ''.join(activity)		

		edu = driver.find_elements_by_xpath("//ul[starts-with(@class,'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more')]")
		edu = [x.text for x in edu]
		edu = ''.join(edu)		

		skills = driver.find_elements_by_xpath("//ol[starts-with(@class,'pv-skill-categories-section__top-skills pv-profile-section__section-info section-info pb1')]")
		skills = [x.text for x in skills]
		skills = ''.join(skills)		

		interests = driver.find_elements_by_xpath("//ul[starts-with(@class,'pv-profile-section__section-info section-info display-flex justify-flex-start overflow-hidden')]")
		interests = [x.text for x in interests]
		interests = ''.join(interests)		

		url = driver.current_url

		# validating if the fields exist on the profile
		name = validate_field(name)
		headline = validate_field(headline)
		location = validate_field(location)
		headings = validate_field(headings)
		highlights = validate_field(highlights)
		summary = validate_field(summary)
		activity = validate_field(activity)
		edu = validate_field(edu)
		skills = validate_field(skills)
		interests = validate_field(interests)
		url = validate_field(url)

		# writing the corresponding values to the header
		writer.writerow([name.encode('utf-8'),
                 headline.encode('utf-8'),
                 location.encode('utf-8'),
                 headings.encode('utf-8'),
                 highlights.encode('utf-8'),
                 summary.encode('utf-8'),
                 activity.encode('utf-8'),
                 edu.encode('utf-8'),
                 skills.encode('utf-8'),
                 interests.encode('utf-8'),
                 url.encode('utf-8')])

		print(name, ":Done")

link_list = mynewlist[400:500]

save(link_list)

driver.quit()