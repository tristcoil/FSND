import os
import json
from flask import request, _request_ctx_stack, Flask, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from dotenv import load_dotenv

# get vars from .env file
load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN') 
ALGORITHMS   = os.getenv('ALGORITHMS') 
API_AUDIENCE = os.getenv('API_AUDIENCE') 



## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():

    incoming_headers = request.headers
    print('--- incoming_headers: ', incoming_headers)

    #incoming_headers look like this:  
    #Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFtVXQ3UG1wbFJ0NkZQQm1WN1Z0dSJ9.eyJpc3MiOiJodHRwczovL2Rldi1tamhiYmE2YS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjExNDFjNDQ1NGUwMzIwMDY5MWU1ZDY0IiwiYXVkIjoibXlhcGkiLCJpYXQiOjE2Mjg3MTMzOTksImV4cCI6MTYyODcyMDU5OSwiYXpwIjoiakpoY1F1NHdzMVlYQkFDTnhGUGdsQkoyS3pJU2IxMnciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDppbWFnZXMiLCJwb3N0OmltYWdlcyJdfQ.J6krKh4ZLPLv-D0ozMe9ifTBsaEpdGPNqjfDZJL6t9TK7eXO9vVkwX2UacqQ2le5YPU_8p6iIfhRXzGmZsRmtxy7QvMHTn2ElhJd8DTN_pEPBcZd5j3bo-j29ybW4QN8jReXbgtZs9J3z8tmuCXJvxHtdRrZ9XTk2bLLz_yLQY0PLDrSLVqM3cOvWDT4LlVerFIMO1EMsyo0p6s_bVNrSM4TruEJqed4zOMPUwMA1RVxKXlmLK8AhOVMtuJu5ZJAyCtuNvwVw1i6KBCNjI1bek68LVxD-tOOg3m_Kr-LYayx9OZU40jReWzBajnYwzAMSYHqNqqwfApGmwIWRKWN1A
    #User-Agent: PostmanRuntime/7.28.4
    #Accept: */*
    #Postman-Token: f8bd58f9-5b3f-4d1d-8df1-2f11f9572b10
    #Host: localhost:5000
    #Accept-Encoding: gzip, deflate, br
    #Connection: keep-alive


    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    # they are space separated
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)    

    if len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)            

    if len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401) 


    token = parts[1]
 
    return token




def check_permissions(permission, payload):

    print('---payload---:', payload)
    print('---permission---:', permission)


    if permission == '':
        print('this is public endpoint, continuing')
    else:

        #raise Exception('Not Implemented')
        if 'permissions' not in payload:
            raise AuthError({'code': 'invalid_claims',
                             'description': 'permissions missing in JWT token'}, 
                             400
                           )
    
        if permission not in payload['permissions']:
            raise AuthError({'code': 'unauthorized',
                             'description': 'permissions missing'}, 
                             403
                           )
    
    return True





def verify_decode_jwt(token):
    #raise Exception('Not Implemented')

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    
    # check contents for keys
    if 'kid' not in unverified_header:
        raise AuthError({'code': 'invalid_header',
                         'description': 'auth header invalid'},
                         401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {'kty': key['kty'],
                       'kid': key['kid'],
                       'use': key['use'],
                       'n': key['n'],
                       'e': key['e']
                      }

    if rsa_key:
        try:
            payload = jwt.decode( token, 
                                  rsa_key,
                                  algorithms=ALGORITHMS,
                                  audience=API_AUDIENCE,
                                  issuer='https://' + AUTH0_DOMAIN + '/'
                                )
            return payload
            
        except jwt.ExpiredSignatureError:
            raise AuthError({'code': 'token_expired',
                         'description': 'JWT auth token expired'},
                         401)
        except jwt.JWTClaimsError:
            raise AuthError({'code': 'invalid_claims',
                         'description': 'Invalid claims in token'},
                         401)                
        except Exception:
            raise AuthError({'code': 'invalid_header',
                             'description': 'Error parsing JWT token'},
                             400)
        

    else:
        raise AuthError({'code': 'invalid_header',
                         'description': 'RSA key not found'},
                         400)





# we need to use extended decorator, 
# since we are passing permission as argument
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        
        #print('---wrapper---', wrapper)
        
        return wrapper
    return requires_auth_decorator        

 

    
