#Using basic authentication and disabling SSL certificate checking

def get_panos_config_api(task):
    scheme = 'https://'
    host = task.host.hostname
    path = '/api/?type=export&category=configuration'
    url = f'{scheme}{host}{path}'
    auth = (task.host.username, task.host.password)
    verify = False
    task.run(task=http_method, url=url, auth=auth, verify=verify)
