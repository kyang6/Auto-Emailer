# Auto-Emailer
Automatic Emailer for use with Gmail accounts

### Make sure requirements are installed using: pip install -r requirements.txt

# Parameters
contacts_file - name of the json file. Example- chevron.txt
file_type- the type of file that contacts_file is. Currently only JSON is supported
username_email- gmail email used to auto login if so desired (Required for auto_login)
password- gmail password used to auto login if so desired (Required for auto_login)
email_body - an array of lines that will be joined with \n\n later. Example
~~~~
    ['Hey __receiver__,',
    'I\'m __sender_name__, a fellow Stanford student studying computer science. I\'m working on an intense 
    class project where we interview professionals to find needs and problems in industries, and later 
    build software solutions for free.',
    '__misc__',
    'I would love to be able to talk to you!',
    'Thanks so much,',
    '__sender_name__']
~~~~
subject_line - subject line
sender_name - The name of the person who is sending the email.
path_to_driver - Path to chrome driver (Required to work)

# Contacts file 
JSON contacts file should look like this: 
~~~~
[{"emails":["james.zhang@stanford.edu"],"name":"James"}, {"emails":["kevin.yang@stanford.edu"],"name":"Kevin"},{"emails":["william@stanford.edu"],"name":"Will"}] 
~~~~

# How to Use
~~~~
from emailer import Emailer  

msg = [
'Hey __receiver__,',
'I\'m __sender_name__, a fellow Stanford student studying computer science. I\'m working on an intense class project where we interview professionals to find needs and problems in industries, and later build software solutions for free.',
'We\'re trying our best to learn more about different industries out there.',
'It\'d be great to hear about advice, your biggest pain points, and what\'s generally on your mind in regards to your industy. Maybe we can build something together!\n\nWould you have any time to chat on phone? Email is also great too!',
'Thanks so much,',
'__sender_name__'
]

subject = "Test Subject Line"

emailer = Emailer(email_body=msg, subject_line=subject, sender_name="Kevin", contacts_file = "test.txt", \
    path_to_driver="/Users/KevinYang/Documents/chromedriver")

emailer.custom_login()
emailer.send_emails()
~~~~