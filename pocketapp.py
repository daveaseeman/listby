import requests
import re
import json


def get_request_token(consumer_key, redirect_uri):
    request_url = 'https://getpocket.com/v3/oauth/request'
    request_token = requests.post(request_url,
                                  data={'consumer_key': consumer_key,
                                        'redirect_uri': redirect_uri}
                                  )
    request_token = request_token.text.replace('code=', '')
    return request_token


def get_auth_url(request_token, redirect_uri):
    auth_base_url = 'https://getpocket.com/auth/authorize'
    token_param = '?request_token=' + request_token
    redirect_param = '&redirect_uri=' + redirect_uri
    auth_url = auth_base_url + token_param + redirect_param
    return auth_url


def get_access_token(consumer_key, request_token):
    access_url = 'https://getpocket.com/v3/oauth/authorize'
    access_response = requests.post(access_url,
                                    data={'consumer_key': consumer_key,
                                          'code': request_token}
                                    )
    response = re.split(r'[=&]', access_response.text)
    print(response)
    user_info = {'access_token': response[1], 'user_name': response[-1]}
    return user_info


def get_list(consumer_key, access_token, count, tag, state):
    get_url = 'https://getpocket.com/v3/get'
    response = requests.post(get_url,
                             data={'consumer_key': consumer_key,
                                   'access_token': access_token,
                                   'count': count,
                                   'tag': tag,
                                   'state': state}
                             )
    response_data = json.loads(response.text)
    list = response_data['list']
    return list


def save_list(consumer_key, access_token, list):
    add_url = "https://getpocket.com/v3/add"
    save_responses = []
    print(list)
    for item in list:
        print(item)
        url = item['resolved_url']
        print(url)
        save_item = requests.post(add_url,
                                  data={'consumer_key': consumer_key,
                                        'access_token': access_token,
                                        'url': url}
                                  )
        save_responses += save_item
    return save_responses
