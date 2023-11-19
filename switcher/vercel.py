import os

import requests

LIST_DEPLOYMENTS_URL = 'https://api.vercel.com/v6/deployments?projectId={}'
DELETE_ALIAS_URL = 'https://api.vercel.com/v2/aliases/{}'
ADD_DOMAIN_TO_PROJECT_URL = 'https://api.vercel.com/v10/projects/{}/domains'
LIST_PROJECT_DOMAINS_URL = 'https://api.vercel.com/v9/projects/{}/domains/'
REMOVE_DOMAIN_FROM_PROJECT_URL = 'https://api.vercel.com/v9/projects/{}/domains/{}'
LIST_PROJECTS_URL = 'https://api.vercel.com/v9/projects'
HEADERS = {
    'Authorization': f'Bearer {os.environ["VERCEL_API_KEY"]}'
}


def _delete_domain_from_all_projects(domain):
    projects_data = requests.get(LIST_PROJECTS_URL, headers=HEADERS).json()['projects']
    for project_data in projects_data:
        project_id = project_data['id']
        requests.delete(REMOVE_DOMAIN_FROM_PROJECT_URL.format(project_id, domain), headers=HEADERS)


def _add_domain_to_project(project_name, domain):
    return requests.post(
        ADD_DOMAIN_TO_PROJECT_URL.format(project_name),
        headers=HEADERS,
        json={'name': domain}
    ).json()


def assign_domain(domain, project_name):
    _delete_domain_from_all_projects(domain)
    if project_name is not None:
        _add_domain_to_project(project_name, domain)
