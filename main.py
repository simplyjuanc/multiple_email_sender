import os.path
import csv
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

    
## Set up Gmail API client
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_credentials(scopes):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def send_email(gmail_service, email, email_body):
    message = MIMEText(email_body, "plain")
    message["From"] = "juancamilovasquezj@gmail.com"
    message["To"] = email
    message["Subject"] = "Becarios calificados y no remunerados"

    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
            # Send the email
        send_message = gmail_service.users().messages().send(userId="me", body=create_message).execute()
        print(F'Email was sent to {email} with Email Id: {send_message["id"]}')
    except Exception as error:
        print(F'An error occurred: {error}')
        send_message = None


        
creds = get_credentials(SCOPES)
gmail_service = build('gmail', 'v1', credentials=creds)     

with open("contacts.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header

    # Iterate through each row of the CSV file
    for row in csv_reader:
        name, company, email = row
        
        # Customize the email template
        
        email_body = f"""\
Estimado {name}:

Me contacto con usted para consultarle si {company} podría usar la ayuda de un becario calificado y no remunerado.

Nuestra organización premiada, Connect-123, encuentra experiencias locales relacionadas con la carrera para estudiantes internacionales y graduados de las mejores universidades de EE.UU. Nos enfocamos en proyectos y objetivos concretos para que nuestros becarios puedan contribuir de manera significativa en su empresa.

Nuestros servicios son gratuitos para las organizaciones anfitrionas y los solicitantes seleccionados trabajan como becarios no remunerados durante períodos de 8 a 12 semanas. Además, nos encargamos de todos sus requisitos logísticos, incluyendo alojamiento y eventos sociales, y nuestro personal local brinda soporte las 24 horas del día, los 7 días de la semana. La idea detrás de nuestro modelo es que las organizaciones locales obtienen un recurso calificado, de forma gratuita, y que los becarios internacionales obtienen experiencia
laboral real.

Algunos ejemplos de áreas de interés pueden incluir redes sociales, diseño, desarrollo de sitios web, marketing, desarrollo empresarial, contabilidad e investigación.

Si la propuesta les parece interesante, nos encantaría ayudarles a encontrar el becario más adecuado para sus necesidades y definir los objetivos del proyecto.

¡Estaremos encantados de colaborar con ustedes en nuestro próximo programa!

Saludos cordiales,

Laura
"""

        # Set up email components
        send_email(gmail_service, email, email_body)