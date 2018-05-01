import time
import random
import json
import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint


# Make sure requirements are installed using: pip install -r requirements.txt

# JSON contacts file should look like this: [{"emails":["james.zhang@stanford.edu"],"name":"James"},\
#   {"emails":["kevin.yang@stanford.edu"],"name":"Kevin"},{"emails":["william@stanford.edu"],"name":"Will"}] 

class Emailer:
    """ This class leverages gmail to send emails to many contacts at once
    
    How to Use

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
    """
    def __init__(self, contacts_file, cc=[], file_type='JSON', username_email="__None__", password="__None__", \
        email_body="__Default_Email_Body__", subject_line="__Default_Subject_Line__", \
        sender_name = "__Default_Sender_Name__", path_to_driver = "No Path Specified"):
        """
            The parameters are as follows

            contacts_file - name of the json file. Example- chevron.txt
            file_type- the type of file that contacts_file is. Currently only JSON is supported
            username_email- gmail email used to auto login if so desired (Required for auto_login)
            password- gmail password used to auto login if so desired (Required for auto_login)
            email_body - an array of lines that will be joined with \n\n later. Example
                [
                'Hey __receiver__,',
                'I\'m __sender_name__, a fellow Stanford student studying computer science. I\'m working on an intense 
                class project where we interview professionals to find needs and problems in industries, and later 
                build software solutions for free.',
                '__misc__',
                'I would love to be able to talk to you!',
                'Thanks so much,',
                '__sender_name__'
                ]

            subject_line - subject line
            sender_name - The name of the person who is sending the email.
            path_to_driver - Path to chrome driver (Required to work)
        """
        self.file_name = contacts_file
        if(self.file_name.rsplit(".",1)[-1]=="csv"):
            file_type = 'CSV'

        self.contacts = []
        if file_type == 'JSON':
            self.file_type = 'JSON'
            try:
                contacts_file = open(contacts_file,'r').read()
                self.contacts = json.loads(contacts_file)
            except:
                print("Error reading in JSON file", sys.exc_info()[0])
        elif file_type == 'CSV':
            try:
                self.read_csv()
            except:
                print("Failed reading in CSV file", sys.exc_info()[0])

        self.username_email = username_email
        self.password = password

        self.driver = webdriver.Chrome(path_to_driver)

        self.subject_line = subject_line
        self.email_body = email_body
        self.sender_name = sender_name
        self.cc = cc

    # Reads in contacts from a CSV file. Look at the provided example for a sample.
    def read_csv(self):
        with open(self.file_name, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.contacts.append({"name":row['name'], "emails":row['emails'].split(",")})

    # Login to custom email. You need to type in your own information and login
    # You have timeout_time seconds to login before timeout
    def custom_login(self):
        self.driver.get("https://mail.google.com/?ui=html")
        timeout_time = 60
        print("You have {0} seconds to login".format(str(timeout_time)))
        try:
            element = WebDriverWait(self.driver, timeout_time).until(
                EC.title_contains("-")
            )
        finally: 
            print("Gmail loaded and ready")
            self.driver.get("https://mail.google.com/?ui=html")

    # Sends one email to email_address with subject and body and cc 
    def send_email(self, email_addresses, subject, body, cc):
        print("Sending emails to {} contacts.".format(len(self.contacts)))

        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.title_contains("- Inbox")
            )
        finally: 
        	print("Gmail loaded and ready")

        compose = self.driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[1]/table[1]/tbody/tr[1]/td/b/a")
        compose.click()
        
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.ID, "to"))
            )
        finally: 
            print("Compose page loaded and ready")

        to_area = self.driver.find_element_by_id("to")
        for email in email_addresses:
            to_area.send_keys(email)
            to_area.send_keys(", ")

        cc_area = self.driver.find_element_by_id("cc")
        for email in cc:
            cc_area.send_keys(email)
            cc_area.send_keys(", ")

        subject_area = self.driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/form/table[2]/tbody/tr[4]/td[2]/input")
        subject_area.send_keys(subject)

        body_area = self.driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/form/table[2]/tbody/tr[8]/td[2]/textarea")
        body_area.send_keys(body)

        send_button = self.driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/form/table[1]/tbody/tr/td/input[1]")

        # Wait random number of milliseconds before sending
        time.sleep(random.uniform(0, 1))
        send_button.click()
    
    # Returns a template email. 
    def email_template(self, receiver="__None__", misc="__None__", clean_receiver=False):
        if clean_receiver:
            receiver = receiver.replace('Ms.', '').replace('Mr.', '').replace('Dr.', '').strip().split(' ')[0]
        
        msg = self.email_body

        msg = '\n\n'.join(msg)
        msg = msg.replace("__receiver__", receiver)
        msg = msg.replace("__sender_name__", self.sender_name)
        msg = msg.replace("__misc__", misc)

        return msg

    # Automatically logs in 
    def auto_login(self):
        if self.username_email == "__None__" or self.password == "__None__":
            print("auto_login requires a username_email and a password." \
                " Make sure to provide both during instantiation.")
            exit()

        print("auto_login is not recommended. Be wary, as your password will be in plaintext")

        self.driver.get("https://mail.google.com/?ui=html")

        emailid=self.driver.find_element_by_id("identifierId")
        emailid.send_keys(self.username_email)

        next_button = self.driver.find_element_by_id('identifierNext')
        next_button.click()
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
        finally: 
            print("Password page loaded")

        password = self.driver.find_element_by_id("password").find_element_by_tag_name("input")
        password.send_keys(self.password)
        sign_in = self.driver.find_element_by_id("passwordNext")
        sign_in.click()

        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.title_contains("Do you really want to use HTML Gmail?")
            )
        except:
            print("Simple HTML page not shown.")
        else:
            confirm_html = self.driver.find_element_by_css_selector("input[type='submit']")
            confirm_html.click()

        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.title_contains("Gmail - Inbox")
            )
        finally: 
            print("Gmail loaded and ready")
            self.driver.get("https://mail.google.com/?ui=html")

    def send_emails(self):
        print("Sending emails...")
        for contact in self.contacts:
            if len(contact['emails'])==0: continue
            
            if 'misc' in contact:
                misc = contact['misc']
            else:
                misc = "__None__"
            if 'name' in contact:
                receiver = contact['name']
            else:
                receiver = "__None__"

            mail_temp = self.email_template(receiver=receiver,misc=misc)

            self.send_email(contact['emails'], self.subject_line, mail_temp, self.cc)
            print("Email sent to {0} at {1}".format(contact['name'],str(contact['emails'])))

# ---------------------------------------------------------- #
def main():
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

if __name__ == "__main__":
    main()










