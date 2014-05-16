#!/usr/bin/python
try:
	from selenium import webdriver
except ImportError:
	print("Selenium is required for this script. Run 'easy_install selenium' or 'pip install selenium' to install this.")
	exit(1)

from random import randrange, choice
from time import sleep
import argparse

parser = argparse.ArgumentParser(description='Fill in survey forms on the Club Nintendo website.')
parser.add_argument('-e', '--email', type=str, required=True, help='Email address to log in with.')
parser.add_argument('-p', '--password', type=str, required=True, help="The password to use for the login.")
parser.add_argument('-b', '--browser', type=str, default='firefox', help="Which browser to use (supported: chrome|firefox, default firefox)")

args = parser.parse_args()

form_url = "https://www.nintendo.co.uk/NOE/en_GB/club_nintendo/mygamesandsystems_p3_do.jsp"

form_elements = {
	'login_userid':					"login_username",
	'login_password':				"login_password",
	'pager_links':					'number',
	'survey_links':					'survey-link',
	'xpath_survey_questions':		"//input[@type='checkbox'] | //input[@type='radio']",
	'age_box':						"q4"
	}

strings = {
	'login_form_show':		"MEMBER LOGIN",
	'logout':				"LOGOUT",
	'register_text':		"Claim Stars",
	'review_site':			"Independent news or review website",
	'survey_title':			"Software survey",
	'survey_submit':		"SUBMIT",
	'survey_complete_url':	"surveyConfirmation.do"
}

if args.browser == 'chrome':
	driver = webdriver.Chrome()
else:
	driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get(form_url)

driver.find_element_by_partial_link_text(strings["login_form_show"]).click()
driver.find_element_by_id(form_elements["login_userid"]).send_keys(args.email)
driver.find_element_by_id(form_elements["login_password"]).send_keys(args.password)
driver.find_element_by_id(form_elements["login_password"]).submit()

driver.find_element_by_partial_link_text(strings["logout"])

driver.get(form_url)
registration_page = driver.current_url

items_per_page = driver.find_element_by_name("itemsPerPage")
for option in items_per_page.find_elements_by_tag_name('option'):
	if option.text == "100": option.click()

pager_links = driver.find_elements_by_class_name(form_elements["pager_links"])
max_page = max(1, len(pager_links))

# loop through pages
for page in range(0, max_page):

	survey_links = driver.find_elements_by_class_name(form_elements["survey_links"])
	while len(survey_links) > 0:
		print(str(len(survey_links)) + " surveys left to complete...")
		driver.find_element_by_class_name(form_elements["survey_links"]).click()
		try:
			all_elements = driver.find_elements_by_xpath(form_elements["xpath_survey_questions"])
			age_box = driver.find_element_by_id(form_elements["age_box"])
		except NoSuchElementException:
			# TODO: handle the single-page survey for big downloads (?)
			print("Can't handle this type of survey! Please fill it in manually and try running the script again.")
			exit(1)
		while driver.title[:len(strings["survey_title"])] == strings["survey_title"]:
			elements = [e for e in all_elements if e.is_displayed()]
			if elements:
				choice(elements).click()
			if age_box.is_displayed():
				age_box.send_keys(str(randrange(13, 90)))
			try:
				driver.find_element_by_partial_link_text(strings["survey_submit"])
				driver.execute_script("submit();")
				break
			except:
				driver.execute_script("next();")

		driver.get(registration_page)
		items_per_page = driver.find_element_by_name("itemsPerPage")
		for option in items_per_page.find_elements_by_tag_name('option'):
			if option.text == "100": option.click()

	pager_links = driver.find_elements_by_class_name(form_elements["pager_links"])
	if len(pager_links) > page:
		pager_links[page+1].click()

driver.quit()
print("All surveys completed.")
