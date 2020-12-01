#!/usr/bin/python3
import os
import re
import requests
import json
import subprocess

from datetime import datetime

USERNAME = ''
TOKEN = ''
REPOSITORY = ''
HEADERS = ''

def set_up():
	'''
	Sets up REPOSITORY and HEADERS
	'''

	global REPOSITORY
	global HEADERS

	repository_cmd = "basename -s .git `git config --get remote.origin.url`"
	repository_output = subprocess.Popen(repository_cmd, shell=True, stdout=subprocess.PIPE)
	
	REPOSITORY = repository_output.communicate()[0].decode("utf-8").strip()
	HEADERS = { 'Authorization': TOKEN }


def get_files_changed(commit_hash):
	'''
	Get the files changed in each commit
	'''

	files_cmd = "git diff-tree --no-commit-id --name-only -r " + commit_hash
	files_output = subprocess.Popen(files_cmd, shell=True, stdout=subprocess.PIPE)

	return files_output.communicate()[0].decode("utf-8")


def push_comment(comment, issue_number):
	'''
	Sends the comment to the corresponding issue
	Uses GitHub API
	'''

	data = { 'body': comment }
	urlComment = "https://api.github.com/repos/" \
		 + USERNAME + "/" \
		 + REPOSITORY + \
		 "/issues/" \
		 + issue_number \
		 + "/comments"

	requests.post(urlComment, data=json.dumps(data), headers=HEADERS)


def commit_push_comments():
	'''
	Main function to send all comments to corresponding issues
	'''

	# gets the current branch
	branch_cmd = "git branch -vv"
	branch_cmd_output = subprocess.Popen(branch_cmd, shell=True, stdout=subprocess.PIPE)
	branch = branch_cmd_output.communicate()[0].decode("utf-8").split('[')[1].split(':')[0]

	# gets all unpushed commits
	commits_cmd = "git log %s..HEAD"%(branch)
	commits_cmd_output = subprocess.Popen(commits_cmd, shell=True, stdout=subprocess.PIPE)
	commits_output = commits_cmd_output.communicate()[0].decode("utf-8")
	
	# removes the empty lines
	commits_output = re.sub(r'\n\s*\n', '\n', commits_output, flags=re.MULTILINE).split('\n')

	i = 0
	issue_number = ''
	files_changed = ''
	comment = ''

	# creates the comment for each commit
	for line in commits_output:
		if(i == 4):
			comment += '\n:memo: **Files changed:** \n' + files_changed
			push_comment(comment, issue_number)
			files_changed = ''
			comment = ''
			i = 0

		if (i == 0 and line):
			commit_hash = line.split()[1]
			files_changed = get_files_changed(commit_hash)
			i += 1
			continue

		if (i == 1):
			author = line.split(':')
			author = author[1].split('<')
			comment += ":bust_in_silhouette: **Commit author:** " + author[0].strip() + "\n"
			i += 1
			continue

		if (i == 2):
			data = line.split()
			data = data[1] + " " + data[2] + " " + data[3] + " " + data[4] + " " + data[5]
			comment += ":clock3: **Date and hour:** " + data + "\n"
			i += 1
			continue

		if (i == 3):
			issue_number = re.search(r'#(\d+)', line).group().replace('#', '')
			comment += ":speech_balloon: **Commit description:**\n'" + line + "'\n"
			i += 1
			continue

	# one empty line stil remains at the end of the list -_-
	commits_output = list(filter(lambda x: x != '', commits_output))

	# number of commits involved in the push
	commits_number = int(len(commits_output)/4)

	# the push comment itself 
	comment = 'The user :bust_in_silhouette:[' + USERNAME \
		 + '](https://github.com/' + USERNAME \
		 + ') made a push at this repo at ' \
		 + datetime.now().strftime("%d/%m/%Y %H:%M:%S") \
		 + '\n\n:information_source: **' + str(commits_number) + ' commits** have been submitted.'

	push_comment(comment, issue_number)


if __name__ == "__main__":
	set_up()
	commit_push_comments()