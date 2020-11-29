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
	global REPOSITORY
	global HEADERS

	repository_cmd = "basename -s .git `git config --get remote.origin.url`"
	repository_output = subprocess.Popen(repository_cmd, shell=True, stdout=subprocess.PIPE)
	REPOSITORY = repository_output.communicate()[0].decode("utf-8").strip()
	HEADERS = { 'Authorization': TOKEN }


def push_comment(comment, issue_number):
	data = { 'body': comment }
	urlComment = "https://api.github.com/repos/" + USERNAME + "/" + REPOSITORY + "/issues/" + issue_number + "/comments"
	print(urlComment)
	requests.post(urlComment, data=json.dumps(data), headers=HEADERS)


def commit_push_comments():
	branch_cmd = "git branch -vv"
	branch_output = subprocess.Popen(branch_cmd, shell=True, stdout=subprocess.PIPE)
	branch = branch_output.communicate()[0].decode("utf-8").split('[')[1].split(':')[0]
	
	commits_cmd = "git log %s..HEAD"%(branch)
	commits_output = subprocess.Popen(commits_cmd, shell=True, stdout=subprocess.PIPE)
	commits_name_output = commits_output.communicate()[0].decode("utf-8")
	commits_name_output = re.sub(r'\n\s*\n', '\n', commits_name_output, flags=re.MULTILINE).split('\n')

	i = 0
	issue_number = ''
	comment = ''

	for line in commits_name_output:
		if(i == 4):
			push_comment(comment, issue_number)
			i = 0
			comment = ''

		if (i == 0):
			# commitHash = line.split()
			# comment += commitHash[1] + "\n"
			i += 1
			continue

		if (i == 1):
			author = line.split(':')
			author = author[1].split('<')
			comment += "Commit author: " + author[0].strip() + "\n"
			i += 1
			continue

		if (i == 2):
			data = line.split()
			data = data[1] + " " + data[2] + " " + data[3] + " " + data[4] + " " + data[5]
			comment += "Date and hour: " + data + "\n"
			i += 1
			continue

		if (i == 3):
			issue_number = re.search(r'#(\d+)', line).group().replace('#', '')
			comment += "Commit description:\n'" + line + "'\n"
			i += 1
			continue


	comment = 'The user ' + USERNAME + ' made a push at this repo at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	push_comment(comment, issue_number)


if __name__ == "__main__":
	set_up()
	commit_push_comments()