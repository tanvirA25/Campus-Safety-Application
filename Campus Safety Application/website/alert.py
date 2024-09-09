import smtplib
from email.message import EmailMessage 

from .models import Report, User

# alerts system using EmailMessage
def alerts_email(subject, body, to):
    alert = EmailMessage()
    alert.set_content(body)
    alert['subject'] = subject
    alert['to'] =to
    
    user = "campussafety.official@gmail.com"
    alert['from'] = user
    password = "lpfpunyjftbinnrc"
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(alert)
    
    server.quit()
    
    # gets the information from report database formats annds sends to all users
def send():
    last_alert = Report.query.order_by(Report.id.desc()).first()
    location = last_alert.location
    formatted_location = location.replace(" ",'+')
    print(formatted_location)
    google_maps_url = f"https://www.google.com/maps/search/{formatted_location}"
    
    body = f"""Date = { last_alert.time }
Level of Severity = { last_alert.level }
Location = { last_alert.location }
Click on this link to view location = {google_maps_url}
                             
{ last_alert.long_description }

Sincerely
Campus Safety
"""
    all_email = User.query.all()
    
    for email in all_email:
        alerts_email(last_alert.title, body , email.email)
   