import argparse
import sys
import requests
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', type=str, help='user for auth with github')
    parser.add_argument('--password', type=str, help='password for auth with github')
    parser.add_argument('--org', type=str, help='organization that will be checked')
    parser.add_argument('--task', type=str, help='which task to preform? (repo,branches)')
    args = parser.parse_args()
    sys.stdout.write(str(test(args)))


def test(args):
    user = args.user
    password = args.password
    org = args.org
    task = args.task
    print("user : ", user)
    check_param(user)
    print("password : ", len(password) * '*')
    check_param(password)
    git_auth(user, password)
    print('org : ', org)
    check_param(org)
    print('task : ', task)
    check_task(task, org)
    print("good bye!")


def check_param(str):
    if str == None:
        print("you must enter value")
        exit()


def check_task(str, org):
    if str == 'repo':
        repo_list = git_repo(org)
        task_printer(repo_list, str)
    elif str == 'branches':
        branches = git_braches_count(org)
        task_printer(branches, str)
    else:
        print("chose an valid task")
        exit()


def git_auth(user, password):
    response = requests.get('https://api.github.com/user', auth=(user, password))
    if response.status_code == 200:
        print('successfully connect github account')
    else:
        print('An Error has occurred')


def git_repo(org):
    repo_arr = []
    response = requests.get('https://api.github.com/users/' + org + '/repos')
    json_res = json.loads(response.content)
    for res in json_res:
        if res["name"] is not None:
            repo_arr.append(res["name"])
    return repo_arr


def task_printer(list, task):
    print("there's", len(list), task)
    print(list)


def git_braches_count(org):
    repo_list = git_repo(org)
    branches_arr = []
    for repo in repo_list:
        response = requests.get('https://api.github.com/repos/' + org + '/' + repo + '/branches')
        json_res = json.loads(response.content)
        for res in json_res:
            if res["name"] is not None:
                branches_arr.append(res["name"])
    return branches_arr


if __name__ == '__main__':
    main()
