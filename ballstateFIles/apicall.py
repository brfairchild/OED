from urllib3 import BaseHTTPResponse, disable_warnings, PoolManager
from urllib3 import exceptions as url_exceptions
import json

disable_warnings()

def fetch_api_key(apikey_url, username, password):
    """
    returns api key from server. Uses utllib3

    Args:
    apikey_url(str): url to get api token from
    username(str): username to authenticate as
    password(str): password to authenticate with

    Returns:
    apikey(str): apikey to use for retriveing data

    """
    try:
        http = PoolManager(cert_reqs='CERT_NONE')
        resp = http.request(
            "POST",
            apikey_url,
            json={
                "username": username,
                "password": password
            }   
        )
        
    except url_exceptions.RequestError as e:
        print(f"Error fetching page {page}: {e}")
        return e

      
    jresp=resp.json()
    token=jresp.get("accessToken")

    return token



def fetch_api_sets(base_url, token, additional_arg='', start_page=1, page_parm="page"):
    """
    Fetches api sets from pageinaed metasys server. Uses urllib3

    Args:
        base_url (str): base of api endpoint
        token (str): api token to access data
        start_page (int): starting page number (default:1)
        page_param (str): name of page paramater, default:page
        additional_arg (str): additional arguments degault: ''

    Returns:
        list: list of returned data
    """
    http = PoolManager(cert_reqs='CERT_NONE')
    all_data = []
    page = start_page
    reqHeader = {
        'Authorization': 'Bearer '+token
        }

    while True:
        if not additional_arg:
            url = f'{base_url}?{page_parm}={page}'
        else:
            url = f'{base_url}?{page_parm}={page}&{additional_arg}'
        try:
            response = http.request(
                'GET', 
                url, 
                headers = reqHeader
                )
            data = response.json()
            all_data.extend(data["items"])
            if 'next' in data and data['next']:
                page += 1
            else:
                break
        except url_exceptions.RequestError as e:
            print(f"Error fetching page {page}: {e}")
            break
    return all_data

def fetch_api_value(api_url, token, param=''):
    """
    Returns the api response for that url

    Args:
        api_url (str): url to the api call
        token (str): api token for this opperation
        param (str): any aditional parameters the api call needs

    Returns:
        httpresponce object is returned
    """
    if not param:
        url = api_url
    else:
        url = api_url +"?"+param
    
    http = PoolManager(cert_reqs='CERT_NONE')
    reqHeader = {
            'Authorization': 'Bearer '+ token
        }
    try:
        resp = http.request(
            'GET',
            url,
            headers = reqHeader
            )

    except url_exceptions.RequestError as e:
            print(f"Error fetching page {url}: {e}")
            return e
    return resp

def fqr_to_object(api_url, fullyQualifiedReference, token):
    """
    Returns the Object reference for a fullyQualifiedReference

    Args:
        api_url (str): http{s}/{site}/api/{version}
        fullyQualifiedReference (str): The fully qualified reference from metasys for the meter of interest
        token (str): the api token to use

    Returns:
        The object id of the item of interst
    """

    try:
        http = PoolManager(cert_reqs='CERT_NONE')
        url = f'{api_url}/objectIdentifiers?fqr={fullyQualifiedReference}'
        reqHeader = {
            'Authorization': 'Bearer '+ token
            }
        resp = http.request(
            "GET",
            url,
            headers = reqHeader
        )
        idValue = resp.data.decode('utf-8')
        idValue = idValue.strip('"')

    except url_exceptions.RequestError as e:
        print(f"Error fetching page {url}: {e}")
        return e
    
    return idValue
