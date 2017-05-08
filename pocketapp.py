import requests
import re
import json

# These are only needed locally:
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())


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
    user_info = {'access_token': response[1], 'user_name': response[3]}
    return user_info


def get_list(consumer_key, access_token, count, tag):
    get_url = 'https://getpocket.com/v3/get'
    response = requests.post(get_url,
                             data={'consumer_key': consumer_key,
                                   'access_token': access_token,
                                   'count': count,
                                   'tag': tag}
                             )
    parse = json.loads(response.text)
    parsed = parse['list']
    list = "Titles:"
    for item in parsed:
        title = parsed[item]['resolved_title'].encode('utf-8')
        list += "\n" + title
    return parsed
