import requests
from datetime import date, timedelta


def get_trending_repositories(top_size):
    last_week = date.today() - timedelta(days=7)
    params = {'q': 'created:>{}'.format(last_week),
              'sort': 'stars', 'per_page': top_size, 'order': 'desc'}
    repo_url = "/".join(("https://api.github.com", 'search', 'repositories'))
    repositories = requests.get(repo_url, params=params)
    if repositories.ok:
        return None
    return repositories.json()['items']


def get_open_issues_amount(repo_owner, repo_name):
    try:
        issues_url = "/".join(("https://api.github.com",
                               'repos', repo_owner, repo_name, 'issues'))
        issues = requests.get(issues_url)
        return [issue for issue in issues.json() if issue['state'] == 'open']
    except (requests.exceptions.ConnectionError, TypeError):
        return []


def print_issues_info(repository):
    if int(repository["open_issues_count"]) > 0:
        print("But this project has {} issues".format(repository["open_issues_count"]))
        login = repository['owner']['login']
        issues_data = get_open_issues_amount(login, repository['name'])
        if not issues_data:
            print("We could not get information about issues")
        else:
            for issue in issues_data:
                print("Issue title: {} Create at {}".
                      format(issue['title'], issue['created_at']))
    else:
        print("This project have not issues!")


def print_repositories_info(repo_data):
    print("Here are {} most popular repositories for last week:".format(len(repo_data)))
    for repository in repo_data:
        print("-" * 30)
        print("Name: {}".format(repository['name']))
        print("Description: {}".format(repository['description']))
        print("You can look it for address {}".format(repository['html_url']))
        print_issues_info(repository)


if __name__ == '__main__':
    top_size = 20
    repositories = get_trending_repositories(top_size)
    if repositories:

        print_repositories_info(repositories)
    else:
        print("Unfortunately, github is not available now")
