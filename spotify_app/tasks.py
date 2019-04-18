import requests

def get_access_token(request):
    return request.session.get('access_token')
