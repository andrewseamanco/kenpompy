"""
The utils module provides utility functions, such as logging in.
"""

import mechanicalsoup
from bs4 import BeautifulSoup
import pandas as pd
import kenpompy.misc as kpmisc
from math import isnan


def login(email, password):
	"""
	Logs in to kenpom.com using user credentials.

	Args:
		email (str): User e-mail for login to kenpom.com.
		password (str): User password for login to kenpom.com.

	Returns:
		browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com.
	"""

	browser = mechanicalsoup.StatefulBrowser()
	browser.open('https://kenpom.com/index.php')

	# Response page actually throws an error but further navigation works and will show you as logged in.
	browser.get_current_page()
	browser.select_form('form[action="handlers/login_handler.php"]')
	browser['email'] = email
	browser['password'] = password

	response = browser.submit_selected()

	if response.status_code != 200:
		raise Exception(
			'Logging in to kenpom.com failed - check that the site is available and your credentials are correct.')

	return browser

def newWinningPercentageDictionary(browser, season=None):
	ratings_df = kpmisc.get_pomeroy_ratings(browser, season)
	ratings_df = ratings_df.dropna()
	print(ratings_df.columns)
	print(ratings_df)
	ratings_dict = ratings_df.set_index('Team').to_dict()['W-L']
	ratings_dict = {k:v for (k,v) in ratings_dict.items() if k != 'Team'}
	ratings_dict = {k:int(str(v).split("-")[0]) / (int(str(v).split("-")[0]) + int(str(v).split("-")[1])) for (k,v) in ratings_dict.items()}
	return ratings_dict

def calculateTeamRPI(browser, team=None, season=None):
	schedule_df = kpteam.get