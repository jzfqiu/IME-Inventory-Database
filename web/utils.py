"""
Various utility functions
"""


from flask import session

def dprint(content):
    """
    Print to docker-compose log for debugging
    """
    if not isinstance(content, str):
        content = str(content)
    print(content, flush=True)


def get_logged_in_user():
    """
    Get logged in user from session
    """
    return session.get('logged_in_user', None)


def flatten_dict(d):
    """
    Given nested, single-key dict, return a list of all keys and value.
    
    For example: {a: {b: c}} => [a, b, c]

    Does not work for dict with multiple keys.
    """
    res = []
    while isinstance(d, dict):
        k = list(d.keys())[0]
        res.append(k)
        d = d[k]
    res.append(d)
    return res


def clean_equipment_data(data):
    """
    Clean data sent from edit form into database object

    Specifically, convert flattened category list to dict 
    and encapsulate contact information
    """
    data['category'] = [
        data.pop('cat'), 
        data.pop('bucket'), 
        data.pop('item')
    ]
    data['campus'] = [data.pop('campus'), data.pop('department')]
    data['contact'] = {
        "name": data.pop('contact-name'),
        "title": data.pop('contact-title'),
        "email-link": data.pop('contact-email'),
        "tel": data.pop('contact-tel')
    }
    # data['manager_id'] = get_logged_in_user()['_id']
    return data


