import requests
from datetime import date, timedelta


def get_trending_repositories(top_size):
    last_week = date.today() - timedelta(days=7)
    params = {'q': 'created:>{}'.format(last_week),
              'sort': 'stars', 'per_page': top_size, 'order': 'desc'}
    repos = requests.get("https://api.github.com/search/repositories",
                         params=params)
    if repos.status_code == requests.codes.ok:
        return repos.json()['items']
    return None


def get_open_issues_for_repo(repo_owner, repo_name):
    try:
        issues_url = 'https://api.github.com/repos/{}/{}/issues'\
            .format(repo_owner, repo_name)
        issues = requests.get(issues_url)
        return [issue for issue in issues.json() if issue['state'] == 'open']
    except (requests.exceptions.ConnectionError, TypeError):
        return []


def print_info_about_repo(repository):
    print("-" * 30)
    print("Name: {}".format(repository['name']))
    print("Description: {}".format(repository['description']))
    print("You can look it on {}".format(repository['html_url']))


def print_info_about_issues(issues):
    if not issues_data:
        print("We could not get information about issues")
    for issue in issues_data:
        print("Issue title: {} Create at {}".
              format(issue['title'], issue['created_at']))

if __name__ == '__main__':
    top_size = 20
    repo_data = get_trending_repositories(top_size)
    if not repo_data:
        print("Unfortunately, github is not available now")
    else:
        print("Here are {} most popular repositories for last week:"
              .format(len(repo_data)))
        for repository in repo_data:
            print_info_about_repo(repository)
            if int(repository["open_issues_count"]) > 0:
                print("But this project has {} issues".format(
                    repository["open_issues_count"]))
                login = repository['owner']['login']
                issues_data = get_open_issues_for_repo(
                    login, repository['name'])
                print_info_about_issues(issues_data)
            else:
                print("This project has not issues!")
