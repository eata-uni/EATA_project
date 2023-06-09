from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

def start_login():
    directorio_credentiales = 'credentials_module.json'   
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credentiales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credentiales)
    else:
        gauth.Authorize()
        return GoogleDrive(gauth)
