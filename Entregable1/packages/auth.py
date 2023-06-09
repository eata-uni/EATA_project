from pydrive2.auth import GoogleAuth

def start():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile('credentials_module.json')

