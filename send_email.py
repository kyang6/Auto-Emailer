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

emailer = Emailer(email_body=msg, subject_line=subject, sender_name="Me", contacts_file = "test.json", \
    path_to_driver="/Users/zihua/Documents/include.ai/emailer_scraper/chromedriver")

emailer.custom_login()
emailer.send_emails()

