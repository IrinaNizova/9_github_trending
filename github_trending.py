import requests
from datetime import date, timedelta


def get_trending_repositories(top_size):
    last_week = date.today() - timedelta(days=7)
    params = {'q': 'created:>{}'.format(last_week),
              'sort': 'stars', 'per_page': top_size, 'order': 'desc'}
    repositories = requests.get("https://api.github.com/search/repositories", params=params)
    if repositories.status_code == requests.codes.ok:
        return repositories.json()['items']
    return None


def get_open_issues_for_repo(repo_owner, repo_name):
    try:
        issues_url = 'https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name)
        issues = requests.get(issues_url)
        return [issue for issue in issues.json() if issue['state'] == 'open']
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
            print("But this project has {} issues".format(repository["open_issues_count"]))
            login = repository['owner']['login']
            issues_data = get_open_issues_for_repo(login, repository['name'])
            if not issues_data:
                print("We could not get information about issues")
            else:
                for issue in issues_data:
                    print("Issue title: {} Create at {}".
                          format(issue['title'], issue['created_at']))
        else:
            print("This project have not issues!")


if __name__ == '__main__':
    repositories = get_trending_repositories(20)
    if repositories:

        print_repositories_info(repositories)
    else:
        print("Unfortunately, github is not available now")
