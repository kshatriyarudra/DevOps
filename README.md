# This project is named as ELK Python Automation.

# About Task:

1.Develop a module in Python to access Elastic Search DB and access the data.

a)For any particular hour measure the count of documents in that hour.

b)For any response time measure the count of documents in that interval.

2.Implement below things next :-

a) Put below details in config file and import the config file.
IP, Port,  Username, Password, Start date time, End date time, Index.

b) Build a program to send email.
You can create and use a fresh Gmail id for this.

c) Send the Count calculated in above program via email.

# Details and steps for this project.

1. Install VS Code and choose language as python and left all as default.

2. After installation you have to make .py file for coding process

3. In .py file you have to use 'pip install elasticsearch' which will download all configuration from elastic search.

4. Import few library in this .py file which is mentioned below.
a) import logging
b) from elasticsearch import Elasticsearch
c) import json
d) import send_mail
e) import query

5. After you cane make another file 'json' which includes your all required credential's.

6. Then you need query so make another file as 'query.py' which includes your query for the given data
and try to use some filter's in this so that you will get proper details from this.

7. When you will be able to login in elastic search you can easily access data and index from any index.

8.When you got valuable information by using some python code in .py file you have to send data to your team then you 
have to make another file as 'send_mail.py' which will send data to the team.

9. For sending data to team you have to take email id's (not limitation's) in csv file and use logging to show the error and critical information.

10. After all this set up just run your .py file and see the details in log file i.e. email is send or not, is there any error while connecting to elastic search,
is there any error for counting documents, to see your documents information etc . 




 
