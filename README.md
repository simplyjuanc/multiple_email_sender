## README.md

### Overview
This code is designed to send customized emails to a list of contacts stored in a CSV file. 
The email's subject and body can be customized based on user input, and the code will append each contact's name, email address, and a timestamp to a log file. 
This code also requires some additional files, which are located in the "input" and "assets" directories.

### Installation
To run this code, you need to have Python 3 installed on your computer. 
Additionally, you will need to install the required packages listed in the "requirements.txt" file using the following command in your terminal:

```
pip install -r requirements.txt
```
OR
```
python3 -m pip install -r requirements.txt
```

### Usage
Once you have installed the required packages, you can run the code by typing the following command in your terminal:

```
python3 main.py 1
```
OR
```
python3 main.py 2
```

The argument "1" or "2" is used to select the CSV file containing the email addresses you want to send the email to, located in the "input" folder. 
If you provide an invalid argument or fail to provide one altogether, the code will display an error message and exit.

### Customization
You can customize the email's subject and body by editing the "email_subject.html" and "email_1_{DATE}.html" or "email_2_{DATE}.html" files located in the "assets" directory. 
The email's signature can also be customized by editing the "signature.html" file located in the same" directory.


### Output
The code will generate a log file in the "logs" directory containing the name, email address, and timestamp for each contact that received the email, along with a message indicating whether the email was successfully sent or not. 
The name of the log file will be automatically generated based on the name of the input CSV file, plus the current datetime. 
E.g. If the CSV file contains the string "first_email" in its name, the log file will be named "logs/contacts_first_email_2023-04-25_19-17-25.csv". 
