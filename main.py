import os
import csv
import sys
import src.utils as utils
from src.config import *



if len(sys.argv) != 2:
    print("ERROR -  Usage: python3 main.py 1 OR python3 main.py 2 ")
    sys.exit()

if sys.argv[1] == '1':
    input_emails = os.path.join(os.getcwd(), 'input', 'contacts_first_email.csv')
    input_file = 'contacts_first_email.csv'[:-4]
elif sys.argv[1] == '2':
    input_emails = os.path.join(os.getcwd(), 'input', 'contacts_second_email.csv')
    input_file = 'contacts_first_email.csv'[:-4]
else:
    print("ERROR -  Usage: python3 main.py 1 OR python3 main.py 2 ")
    sys.exit()


output_path = utils.post_log(input_file)
email_subject, email_body = utils.select_email_elements(sys.argv[1])
sig_html = utils.get_html_asset('signature.html')


with open(input_emails, "r") as csv_file:
    csv_reader = csv.reader(csv_file) 
    next(csv_reader)  # Skip the header
    
    # Customise the email template and send email.
    for row in csv_reader:
        user_message = utils.post_custom_email(
            row, 
            email_body, 
            email_subject, 
            sig_html)
        
        utils.append_log(output_path, row, user_message)
