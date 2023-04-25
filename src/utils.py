import base64
import os
import csv
import datetime
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_credentials(scopes):
    # Load the client_id and client_secret from the client_secrets.json file
    with open(os.path.join(os.getcwd(), ".creds","client_secrets.json"), "r") as f:
        client_secrets = json.load(f)

    creds = None

    # Check if there's a valid token.pickle file
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no valid credentials available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(client_secrets, scopes)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_html_asset(html_file_str):
    """ Read email body file and returns string.
    """
    try:
        file_path = os.path.join(os.getcwd(), 'assets', html_file_str)
        with open(file_path, 'r') as file:
            file_contents = file.read()
        return file_contents
    except FileExistsError as e:
        print(f'ERROR {e}: HTML file not found.')


def select_email_elements(arg):
    """ Retrieves adequate HTML elements as strings from the assets dir. 
    Args:
        - arg: The first command-line argument passed to the script.
    Returns:
        - email_subject (str), email_body (str)
    """
    if arg == '1':
        body_file = 'email_1_2023-04-25.html'
        email_subject = "[[organization]] / Connect-123 Interns"
    elif arg == '2':
        body_file = 'email_2.html'
        email_subject = "Internship follow up"
    else:
        print("Invalid argument. Please enter '1' or '2'.")
        return None
     
    email_body = get_html_asset(body_file)

    return email_subject, email_body


def replace_vars_in_str(var_dict:dict,text:str) -> str:
    """ Replaces [[{var}]]-formatted keys 
    in strings with value in var_dict
    """
    # print(text)
    custom_txt = text
    for k,v in var_dict.items():
        custom_txt = custom_txt.replace('[[{}]]'.format(k), v)
    # print(custom_txt)
    return custom_txt


def send_email(to_email, subject, email_body, signature):
    """
    to_email: str
    subject: HTML object
    email_body: HTML object
    signature: HTML object 
    """
    
    # OAuth2 setup
    creds = get_credentials(scopes=os.getenv('SCOPES'))

    try:
       # Set up Gmail API client
        service = build('gmail', 'v1', credentials=creds)

        # Set up email components
        msg = MIMEMultipart()
        msg["To"] = to_email
        msg["Subject"] = subject
        
        msg.attach(MIMEText(email_body, "html"))
        msg.attach(MIMEText(signature, "html"))

        raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
        message = {"raw": raw_msg}

        # Send the email
        send_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Email sent to {to_email} (Message ID: {send_message['id']})")
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = str(error)

    return send_message


def post_custom_email(csv_row_str, email_body, subject_email, sig_html):
    """ Takes a csv row, customises and sends an email, 
    and returns the system message.
    Args:
     - csv_row_str: csv row with only name, company, email values
     - email_body: HTML body as str
     - subject_email: str
     - sig_html: HTML body as str
    Returns: user_message - Status Code as str"""
    name, company, email = csv_row_str
    cust_dict = {
        'name':name,
        'organization':company,
        'email':email
    }
    
    # Customise the email template
    cust_subject_email = replace_vars_in_str(cust_dict, subject_email)
    cust_email_body = replace_vars_in_str(cust_dict, email_body)
    
 
    # Set up email components
    user_message = send_email(
        email, 
        cust_subject_email, 
        cust_email_body, 
        sig_html
        )
    
    return  # user_message


def post_log(log_name):
    """ Check if logs dir exists and creates it. Writes first row of log.
    Args:
        - log_name: How will it be prefixed - usually it's input_file[:-4] 
    Returns: 
        - ouput_path: Where 
    """
    # Set name for log file
    output_file = "{input_file}_{today}_{time}.csv".format(
        input_file=log_name,
        today=datetime.date.today().strftime('%Y-%m-%d'),
        time=datetime.datetime.now().strftime('%H-%M-%S')
    )

    # Create logs folder if it doesn't exist.
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # And then write header for output (log) file
    output_path = os.path.join(os.getcwd(), 'logs', output_file)
    with open(output_path, 'w') as output_f:
        csv_writer = csv.writer(output_f)
        csv_writer.writerow(['name', 'company', 'email', 'message_status'])
    
    return output_path


def append_log(output_path, csv_row_str, user_message):
    name, company, email = csv_row_str
    with open(output_path, 'a') as output_f:
        csv_writer = csv.writer(output_f)
        csv_writer.writerow([name, company, email, user_message])
