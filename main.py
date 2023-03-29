import sys
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up your email credentials
if len(sys.argv) != 3:
    print('Usage: python3 main.py email_address email_password')
    sys.exit()

EMAIL_ADDRESS = sys.argv[1]
EMAIL_PASSWORD = sys.argv[2]

# Read the CSV file
def send_email(from_address, email_password, to_email, email_body):
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_email
    msg["Subject"] = "Becarios calificados y no remunerados"
    msg.attach(MIMEText(email_body, "plain"))

        # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_address, email_password)
            server.sendmail(from_address, email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")


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
        send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, email, email_body)
