from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
directorio_credentiales = 'credentials_module.json'
# INICIAR SESION
def start_login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credentiales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credentiales)
    else:
        gauth.Authorize()
    return GoogleDrive(gauth)
