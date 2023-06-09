from pydrive2.auth import GoogleAuth

def start_auth():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile('credentials_module.json')

