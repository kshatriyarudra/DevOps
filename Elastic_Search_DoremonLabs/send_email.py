import csv, smtplib, ssl
import config as cfg

message = """Subject: Count details from ELK.
To: {}
Hello {},


Total number of documents in given range of time is: {}
Total number of documents in given range of response time is: {}

Thanks and Regards
ELK Python Automation"""

context = ssl.create_default_context()


def send(count_time, count_response):
    """Sending email to the user's/employee's.

    Parameters:
    count_time (int): Total number of documents in given time interval.
    count_response (int): Total number of documents in given response time.

    Returns: Nothing"""
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(cfg.email_details["from_address"], cfg.email_details["email_password"])
        with open("email_ids.csv") as file:
            reader = csv.reader(file)
            next(reader)
            for name, email in reader:
                server.sendmail(
                    cfg.email_details["from_address"],
                    email,
                    message.format(name, name, count_time, count_response),
                )
            return