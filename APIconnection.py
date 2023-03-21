import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from googleapiclient.discovery import build
import os

os.chdir("YouTube Channel Seeker") #os.getcwd()

# Credenciales de la API de YouTube
# PARA USAR LA API ES NECESARIO TENER CREDENCIALES (CLIENT_SECRET.JSON) Y ACCESO DE DEVELOPER/TESTER. En su defecto, cree su cuenta (https://console.cloud.google.com/), diríjase a Más productos/APIs y servicios/APIs y servicios habilitados/Crear proyecto, diligencie la información, descargue el archivo client_secret.json (client_secret_XXXXCLAVEXXXX.apps.googleusercontent.com.json) y anéxelo a la carpeta actual con el nombre "client_secret.json"
CLIENT_SECRETS_FILE="client_secret.json" #Clave de la API para poder ingresar (obtenido del proceso de registro)
SCOPES=["https://www.googleapis.com/auth/youtube.readonly"] #La acción a la que se dirije (en este caso readonly)/Habilita ciertas operaciones
API_SERVICE_NAME="youtube"
API_VERSION="v3"

def get_authenticated_service():
    flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES) #Integra request y abre navegador para autenticarse con cuenta gmail
    credentials=flow.run_local_server(port=0)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials) #Retorna archivo con toda la información

def get_subscriptions():
    youtube=get_authenticated_service()
    subscriptions=[]
    request=youtube.subscriptions().list(
        part="snippet", #Solicitar llamada a la API. Devuelve información básica (canal, video, lista de reproducción)
        mine=True,
        maxResults=500 #Cantidad máxima de resultados/consultas que se permiten hacer
    ) #Obtener lista de suscripciones

    while request is not None:
        response=request.execute()
        for item in response["items"]:
            title=item["snippet"]["title"]
            channel_id=item["snippet"]["resourceId"]["channelId"] #Petición al servidor de Google. Extrae información del channelID
            link=f"https://www.youtube.com/channel/{channel_id}"
            category = item["snippet"].get("categoryId", "Not available") #Obtiene la categoría y, en caso de no tener, la deja 'Not available'
            subscription=[title, link, category]
            subscriptions.append(subscription)
        request = youtube.subscriptions().list_next(request, response)
    return subscriptions

def print_subscriptions(subscriptions):
    for subscription in subscriptions:
        print(f"Nombre del canal: {subscription['title']}")
        print(f"Link del canal: {subscription['link']}")
        print(f"Categoría del canal: {subscription['category']}", end="\n\n")

'''
# Ejemplo de uso
subscriptions = get_subscriptions()
print_subscriptions(subscriptions)

# Ejemplo de uso
filename = input("Ingrese el nombre del archivo: ")
try:
    with open(filename, 'a') as f:
        subscriptions = get_subscriptions()
        for subscription in subscriptions:
            f.write(subscription)
        print("Información guardada correctamente.")
except Exception as e:
    print(f"Error al guardar información en archivo: {e}")
'''