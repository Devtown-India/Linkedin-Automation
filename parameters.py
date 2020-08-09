""" filename: paraeters.py"""

# search query
search_query = 'site:linkedin.com/in/ AND "python developer" AND "London"'

# file were scraped profile information will be stored
file_name = 'results_file.csv'

# login credentials
linkedin_username = 'XXXXXXXXX'
linkedin_password = 'XXXXXXXXX'

# function to ensure all key data fields have a value
def validate_field(field):
	# if field is present pass 
	if field:
		pass
	# if field is not present print text 
	else:
		field = 'No results'
	return field