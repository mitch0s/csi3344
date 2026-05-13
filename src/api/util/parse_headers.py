

def parse_authorization_header(headers:dict) -> str|None:
    """
    Parse and return the api token as a string from raw headers
    :headers: dictionary representing key-value header values
    :returns: string containing api token, or None if header does not exist.
    """
    # get auth header, default to None
    auth_header = headers.get('Authorization', None)
    # return early if header value is None
    if auth_header is None: 
        return None
    
    #         v Note the space here
    if 'bearer ' not in auth_header.lower():
        return None

    auth_scheme, auth_token = auth_header.split(' ')

    return auth_token 