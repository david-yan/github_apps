import requests
import sys
from datetime import datetime
from datetime import timedelta

repos_request = requests.get('https://api.github.com/users/' + sys.argv[1] + '/repos')
repos_json = repos_request.json()

today = datetime.today()
delta = timedelta(days=365)
since = (today - delta).isoformat().split('.')[0]
contributions = {}
for repo in repos_json:
	commit_request = requests.get('https://api.github.com/repos/' +sys.argv[1] + '/' + repo['name'] + '/commits?since=' + since)
	issues_request = requests.get('https://api.github.com/repos/' + sys.argv[1] + '/' + repo['name'] + '/issues?since=' + since)
	commits_json = commit_request.json()
	issues_json = issues_request.json()
	for commit in commits_json:
		d = commit['commit']['committer']['date']
		day = datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ")
		diff = (today - day).days
		if diff in contributions:
			contributions[diff] = contributions[diff] + 1
		else:
			contributions[diff] = 1

	for issue in issues_json:
		if issue['user']['login'] == sys.argv[1]:
			d = issue['created_at']
			day = datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ")
			diff = (today - day).days
			if diff in contributions:
				contributions[diff] = contributions[diff] + 1
			else:
				contributions[diff] = 1
print(contributions)
