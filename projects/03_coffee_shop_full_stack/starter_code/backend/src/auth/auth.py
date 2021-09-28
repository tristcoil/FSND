import json
from flask import request, _request_ctx_stack, Flask, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


#AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
#ALGORITHMS = ['RS256']
#API_AUDIENCE = 'dev'


AUTH0_DOMAIN = 'dev-mjhbba6a.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'myapi'




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

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    ###raise Exception('Not Implemented')

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







'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
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






'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
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
            payload = jwt.decode( token, rsa_key,
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













'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''

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
        
        return wrapper
    return requires_auth_decorator        


    
#def requires_auth(f):
#    @wraps(f)
#    def wrapper(*args, **kwargs):
#        token = get_token_auth_header()
#        try:
#            payload = verify_decode_jwt(token)
#        except:
#            abort(401)
#        return f(payload, *args, **kwargs)
#    
#    return wrapper            
    
    
    
    
    
# -------------------    

    
    
    
    
    
        
    
    
    
    
    