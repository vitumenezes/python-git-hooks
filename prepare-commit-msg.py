#!/usr/bin/python3

import sys, re, requests, json
from subprocess import check_output

if __name__ == "__main__":
	msgfile = sys.argv[1]

	with open(msgfile) as f:
		contents = f.read()
	
	# regex to validate the commig
	regex = '^(feat|hotfix|chore|test):.* \(#[0-9]+\)$'

	# commit validation
	if re.match(regex, contents):
		print('The commit is on the patterns :)')
	else:
		print('============================================================================')
		print('The commit does not respect the patterns')
		print('\n')
		print('----------------------------------------------------------------------------')
		print("The Pattern is:\n\n(feat|hotfix|chore|test): text of the commit (#issue_number)")
		print('----------------------------------------------------------------------------')
		print('\n')
		print('============================================================================')
		exit(1)

	issue_number = contents.split()
	issue_number = re.search(r'(\d+)', issue_number[-1]).group()
	print(issue_number)

	url = "https://api.github.com/repos/viniciusrsss/GerenciaDeConfiguracaoEMudanca/issues/" + issue_number

	response = requests.get(url)

	if response.status_code != 200:
		print("This issue does not exists. Please check repo for more information.")
		exit(1)

	labels = response.json()['labels']

	doing = False
	for label in labels:
		if label['name'] == 'doing':
			doing = True
			break
	
	if not doing:
		print("This issue has not the 'doing' label. Please check repo for more information.")
		exit(1)
