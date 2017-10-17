import requests
from datetime import date, timedelta

REPOS_NUMBER = 20


def get_github_api_host():
    return "https://api.github.com"


def get_trending_repositories(top_size):
    params = {'q': 'created:>{}'.format(date.today() - timedelta(days=7)),
              'sort': 'stars', 'per_page': top_size, 'order': 'desc'}
    repositories = requests.get("/".join((get_github_api_host(), 'search', 'repositories')), params=params)
    if repositories.status_code != 200:
        return None
    return repositories.json()['items']


def get_open_issues_amount(repo_owner, repo_name):
    try:
        issues = requests.get("/".join((get_github_api_host(), 'repos', repo_owner, repo_name, 'issues')))
        print("/".join((get_github_api_host(), 'repos', repo_owner, repo_name, 'issues')))
        return [bug for bug in issues.json() if bug['state'] == 'open']
    except (requests.exceptions.ConnectionError, TypeError):
        return []


def print_repositories_info(repo_data):
    print("Here are {} most popular repositories for last week:".format(len(repo_data)))
    for repository in repo_data:
        print("-" * 30)
        print("Name: {}".format(repository['name']))
        print("Description: {}".format(repository['description']))
        print("You can look it for address {}".format(repository['html_url']))
        if int(repository["open_issues_count"]) > 0:
            print("But this project has {} bugs".format(repository["open_issues_count"]))
            bugs_data = get_open_issues_amount(repository['owner']['login'], repository['name'])
            for bug in bugs_data:
                print("Bug title: {} Create at {}".format(bug['title'], bug['created_at']))
            if not bugs_data:
                print("We could not get information about bugs")
        else:
            print("This project have not bugs!")


if __name__ == '__main__':
    repositories = get_trending_repositories(REPOS_NUMBER)
    if repositories:
        print_repositories_info(repositories)
    else:
        print("Unfortunately, github is not available now")
