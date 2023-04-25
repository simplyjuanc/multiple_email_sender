import os
import csv
import sys
import src.utils as utils

if len(sys.argv) != 2:
    print("ERROR -  Usage: python3 main.py 1 OR python3 main.py 2 ")
    sys.exit()

if sys.argv[1] == '1':
    input_emails = os.path.join(os.getcwd(), 'input', 'contacts_first_email.csv')
    log_file = 'contacts_first_email.csv'[:-4]
elif sys.argv[1] == '2':
    input_emails = os.path.join(os.getcwd(), 'input', 'contacts_second_email.csv')
    log_file = 'contacts_first_email.csv'[:-4]
else:
    print("ERROR -  Usage: python3 main.py 1 OR python3 main.py 2 ")
    sys.exit()



SCOPES = ['https://www.googleapis.com/auth/gmail.send']


output_path = utils.post_log(log_file)
sig_html = utils.build_signature_html('signature.html')
email_subject, email_body = utils.select_email_elements(sys.argv[1])


with open(input_emails, "r") as csv_file:
    csv_reader = csv.reader(csv_file) 
    next(csv_reader)  # Skip the header
    
    # Customise the email template and send email.
    for row in csv_reader:
        user_message = utils.post_custom_email(row, email_body, email_subject, sig_html)
        utils.append_log(output_path, row, user_message)
