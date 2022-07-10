import requests
from pprint import pprint

us_name = 'octocat'
url = f'https://api.github.com/users/{us_name}/repos'

response = requests.get(url)
j_data = response.json()
print('user name is', us_name)
print('names of repo:')
for elem in j_data:
    pprint(f"{elem.get('full_name')}")
#print()