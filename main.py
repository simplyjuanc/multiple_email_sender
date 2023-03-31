import os.path
import csv
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


    
## Set up Gmail API client
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def build_signature_html(signature_name):
    sig_file_name = signature_name
    sig_file_path = os.path.join(os.getcwd(), 'assets' ,sig_file_name)
    sig_html = ''
    with open(sig_file_path) as f:
        sig_html += ''.join(f.readlines())
    return sig_html


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


def send_email(to_email, email_body, signature):
    """
    to_email: str
    email_body: HTML object
    signature: HTML object 
    """
    
    # OAuth2 setup
    creds = get_credentials(SCOPES)

    try:
        service = build('gmail', 'v1', credentials=creds)

        # Set up email components
        msg = MIMEMultipart()
        msg["To"] = to_email
        msg["Subject"] = "Becarios calificados y no remunerados"
        
        msg.attach(MIMEText(email_body, "html"))
        msg.attach(MIMEText(signature, "html"))

        raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
        message = {"raw": raw_msg}

        # Send the email
        send_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Email sent to {to_email} (Message ID: {send_message['id']})")

    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None

    return send_message



sig_html = build_signature_html('signature.html')


with open("contacts.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header

    # Iterate through each row of the CSV file
    for row in csv_reader:
        name, company, email = row
        
        # Customise the email template
        email_body = f"""
<html>
<head></head>
<body>
<p>Estimado <strong>{name}</strong>:</p>

<p>Me contacto con usted para consultarle si <strong style="color: blue;">{company}</strong> podría usar la ayuda de un becario calificado y no remunerado.</p>

<p>Nuestra organización premiada, <em>Connect-123</em>, encuentra experiencias locales relacionadas con la carrera para estudiantes internacionales y graduados de las mejores universidades de EE.UU. Nos enfocamos en proyectos y objetivos concretos para que nuestros becarios puedan contribuir de manera significativa en su empresa.</p>

<!-- Other paragraphs here -->

<p>Saludos cordiales,</p>
</body>
</html>
"""
        # Set up email components
        send_email(email, email_body, sig_html)