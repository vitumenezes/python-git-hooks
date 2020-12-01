#!/usr/bin/python3
import sys
import re
import requests
import json
import subprocess

USERNAME = ''
REPOSITORY = ''

def set_up():
	'''
	Sets up variable REPOSITORY
	'''
	
	global REPOSITORY

	repository_cmd = "basename -s .git `git config --get remote.origin.url`"
	repository_output = subprocess.Popen(repository_cmd, shell=True, stdout=subprocess.PIPE)
	REPOSITORY = repository_output.communicate()[0].decode("utf-8").strip()


def commit_validation():
	'''
	Validates the last commit
	'''

	# gets the last commit message
	msgfile = sys.argv[1]

	# opens the commit message file 
	with open(msgfile) as f:
		contents = f.read()

	# regex to validate the commit
	regex = '^(feat|hotfix|chore|test):.* \(#[0-9]+\)$'

	# commit validation
	if re.match(regex, contents):
		print('The commit is on the patterns :)')
	else:
		print('============================================================================')
		print('The commit does not respect the patterns')
		print('\n')
		print('----------------------------------------------------------------------------')
		print("The Pattern is:\n\nfeat|hotfix|chore|test: text of the commit (#issue_number)")
		print('----------------------------------------------------------------------------')
		print('\n')
		print('============================================================================')
		exit(1)

	# gets the issue number
	issue_number = contents.split()
	issue_number = re.search(r'(\d+)', issue_number[-1]).group()

	# creates the url to acess the GitHub API
	url = "https://api.github.com/repos/" + USERNAME + "/" + REPOSITORY + "/issues/" + issue_number

	# gets API response
	response = requests.get(url)

	# checks if the issue exists
	if response.status_code != 200:
		print("This issue does not exists. Please check repo for more information.")
		exit(1)

	# gets the issue labels
	labels = response.json()['labels']

	# checks if the issue have the 'doing' label
	doing = False
	for label in labels:
		if label['name'] == 'doing':
			doing = True
			break

	# if not, exits
	if not doing:
		print("This issue has not the 'doing' label. Please check repo for more information.")
		exit(1)


if __name__ == "__main__":
	set_up()
	commit_validation()