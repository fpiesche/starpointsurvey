#!/usr/bin/python
try:
	from selenium import webdriver
	from selenium.common.exceptions import NoSuchElementException
except ImportError:
	print("Selenium is required for this script. Run 'easy_install selenium' or 'pip install selenium' to install this.")
	exit(1)

from random import randrange, choice
import argparse

def get_surveys():
	try:
		survey_links = driver.find_elements_by_xpath(form_elements["survey_links"])
		return [survey.get_attribute("href") for survey in survey_links]
	except NoSuchElementException:
		return []

def next_page():
	try:
		page_link = driver.find_element_by_id(form_elements["next_page"])
		return page_link
	except NoSuchElementException:
		return False

def next_survey_page():
	next_buttons = driver.find_elements_by_xpath(form_elements["xpath_next_button"])
	for button in next_buttons:
		if button.is_displayed():
			button.click()
			return
	raise Exception("Could not find a visible Next button!")

def finish_survey():
	driver.find_element_by_partial_link_text(strings["submit_button"]).click()

def software_survey():
	try:
		all_elements = driver.find_elements_by_xpath(form_elements["xpath_survey_questions"])
		age_box = driver.find_element_by_name(form_elements["age_box"])
	except NoSuchElementException:
		# Is this a page that's just text?
		print("No survey elements found, trying to advance to next page.")
		next_survey_page()

	while driver.title.lower().startswith(strings["software_survey"]):
		all_elements = driver.find_elements_by_xpath(form_elements["xpath_survey_questions"])
		elements = [e for e in all_elements if e.is_displayed()]
		if elements:
			choice(elements).click()
		if age_box.is_displayed():
			age_box.send_keys(str(randrange(13, 90)))
		try:
			finish_survey()
		except NoSuchElementException:
			next_survey_page()

def game_survey():
	try:
		all_elements = driver.find_elements_by_xpath(form_elements["xpath_survey_questions"])
		elements = [e for e in all_elements if e.is_displayed()]
		elem_groups = set([elem.get_attribute("name") for elem in elements])
		elem_groups = list(elem_groups)
	except NoSuchElementException:
		# Is this a page that's just text?
		print("No survey elements found, trying to advance to next page.")
		next_survey_page()

	while driver.title.lower().startswith(strings["game_survey"]) or driver.title.lower().startswith(strings["hardware_survey"]):
		all_elements = driver.find_elements_by_xpath(form_elements["xpath_survey_questions"])
		elements = [e for e in all_elements if e.is_displayed()]
		elem_groups = set([elem.get_attribute("name") for elem in elements])
		elem_groups = list(elem_groups)

		# handle groups of radio buttons on the same page
		for group in elem_groups:
			grp_elem = driver.find_elements_by_xpath(form_elements["xpath_elem_groups"].replace("$GRP$", group))
			choice(grp_elem).click()

		# enter random values into all text fields
		for txt_field in driver.find_elements_by_xpath(form_elements["xpath_text_fields"]):
			if txt_field.is_displayed():
				txt_field.send_keys(str(randrange(13, 90)))

		# select random options from popup selections
		for select in driver.find_elements_by_xpath(form_elements["xpath_select"]):
			if select.is_displayed():
				choice(select.find_elements_by_xpath(form_elements["xpath_options"])).click()

		try:
			finish_survey()
		except NoSuchElementException:
			next_survey_page()


parser = argparse.ArgumentParser(description='Fill in survey forms on the Club Nintendo website.')
parser.add_argument('-e', '--email', type=str, required=True, help='Email address to log in with.')
parser.add_argument('-p', '--password', type=str, required=True, help="The password to use for the login.")
parser.add_argument('-b', '--browser', type=str, default='firefox', help="Which browser to use (supported: chrome|firefox, default firefox)")

args = parser.parse_args()

form_url = "https://www.nintendo.co.uk/NOE/en_GB/club_nintendo/mygamesandsystems_p3_do.jsp"

form_elements = {
	'login_userid':					"login_username",
	'login_password':				"login_password",
	'next_page':					"paging-next-button-h",
	'survey_links':					"//div[contains(@class,'survey-link')]/a",
	'xpath_survey_questions':		"//input[@type='checkbox'] | //input[@type='radio']",
	'xpath_elem_groups':			"//input[@name='$GRP$']",
	'xpath_next_button':			"//a[contains(@href,'next();')] | //a[contains(@href,'submitForm')]",
	'xpath_text_fields':			"//input[@type='text'] | //input[@type='textarea']",
	'xpath_select':					"//select",
	'xpath_options':				"option[@value!='-1']",
	'age_box':						"q4",
	}

strings = {
	'login_form_show':		"MEMBER LOGIN",
	'logout':				"LOGOUT",
	'software_survey':		"software survey",
	'game_survey':			"game survey",
	'hardware_survey':		"hardware survey",
	'submit_button':		"SUBMIT",
}

if args.browser == 'chrome':
	driver = webdriver.Chrome()
else:
	driver = webdriver.Firefox()
driver.implicitly_wait(10)

# get registration page
driver.get(form_url)

# open login form and attempt login
driver.find_element_by_partial_link_text(strings["login_form_show"]).click()
driver.find_element_by_id(form_elements["login_userid"]).send_keys(args.email)
driver.find_element_by_id(form_elements["login_password"]).send_keys(args.password)
driver.find_element_by_id(form_elements["login_password"]).submit()

# verify that we're logged in
try:
	driver.find_element_by_partial_link_text(strings["logout"])
except NoSuchElementException:
	print("Login failed - verify your username and password please!")
	exit(1)

# get the registration page again
driver.get(form_url)
skipped_surveys = []

# build list of survey links
survey_urls = get_surveys()

np_link = next_page()
while np_link:
	np_link.click()
	survey_urls += get_surveys()
	np_link = next_page()

print("Found %s surveys." % len(survey_urls))

# loop over survey links on all subsequent pages
for survey in survey_urls:

	driver.get(survey)

	if driver.title.lower().startswith(strings["software_survey"]):
		software_survey()
	elif driver.title.lower().startswith(strings["game_survey"]) or driver.title.lower().startswith(strings["hardware_survey"]):
		game_survey()
	else:
		print("Unknown survey type! Page title: %s" % driver.title)


driver.quit()
