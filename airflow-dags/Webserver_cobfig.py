from authlib.integrations.flask_client import OAuth

# Define your OIDC settings
OIDC_CLIENT_ID = 'your-client-id'
OIDC_CLIENT_SECRET = 'your-client-secret'
OIDC_DISCOVERY_URL = 'https://your-oidc-provider/.well-known/openid-configuration'

def configure_app(app):
    oauth = OAuth(app)
    oauth.register(
        name='oidc',
        client_id=OIDC_CLIENT_ID,
        client_secret=OIDC_CLIENT_SECRET,
        server_metadata_url=OIDC_DISCOVERY_URL,
        client_kwargs={
            'scope': 'openid email profile',
        }
    )
    return oauth

# Airflow specific settings
AUTH_USER_REGISTRATION = True  # Allow automatic user registration
AUTH_USER_REGISTRATION_ROLE = "Public"  # Default role for newly registered users

def get_user_profile(userinfo):
    return {
        'username': userinfo['email'],
        'email': userinfo['email'],
        'first_name': userinfo['given_name'],
        'last_name': userinfo['family_name'],
    }
