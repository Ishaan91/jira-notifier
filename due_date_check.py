import requests
from requests.auth import HTTPBasicAuth
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from due_date_send_email import send_email

auth = HTTPBasicAuth("ishaan.agrawal@automationanywhere.com", "9MHTJjjeJwTgHICQkEUV6906")
headers = {"Accept": "application/json"}

# url = "https://automationanywhere.atlassian.net/rest/api/3/search?jql=fixVersion%20=%20'IQ%20Bot%2011.3.5.1'%20AND%20issuetype%20in%20(improvement,%20story,%20defect,%20task)%20AND%20('Release%20Notes%20Required'%20=%20Yes%20OR%20'Additional%20Needs'%20=%20'Release%20Note%20Needed')"

list_of_recipients = [
    "ishaan.agrawal",
    "smita.biswas",
    "aditi.gupta",
    "aanubbhaa.jhhaa",
    "vikram.bp"
#     "aditi.kashikar"
                    ]


# list_of_recipients = [
#     "aanubbhaa.jhhaa",
#     "aditi.gupta",
#     "aditi.kashikar",
#     "arthur.hoang",
#     "eve.karp",
#     "gina.baronianmoore",
#     "ishaan.agrawal",
#     "joe.zucker",
#     "kristy.briggs",
#     "michael.mann",
#     "mira.dytko",
#     "priya.mehta",
#     "rugmony.naganathan",
#     "shyam.ramani",
#     "smita.biswas",
#     "srilatha.p",
#     "tejashree.shiju",
#     "vikram.bp"
# ]

def get_due_issues(name):

    url_link = 'https://automationanywhere.atlassian.net/rest/api/3/search?jql='
    url = url_link+"project%20=%20ED%20AND%20'Doc Owner'%20=%20"+name+"%20AND%20due<=%202d%20AND%20status%20!=%20Closed"

    # url = "https://automationanywhere.atlassian.net/rest/api/3/search?jql=project%20=%20ED%20AND%20'Doc Owner'%20=%20ishaan.agrawal%20AND%20due<=%202d%20AND%20status%20!=%20Closed"
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    data = json.loads(response.text)
    issues_due = []
    print "issues_due = ", data["total"]
    for issue in data["issues"]:
        issues_due.append(tuple((issue["key"], issue["fields"]["duedate"], issue["fields"]["status"]["name"])))

    for item in issues_due:
        print item[0], item[1], item[2]

    # send_email(name, list_of_due_issues)
    return issues_due

# ----------------End of method-----------------------


def get_pending_issues(name):

    url_link = 'https://automationanywhere.atlassian.net/rest/api/3/search?jql='
    # url = url_link + "project%20=%20ED%20AND%20'Doc Owner'%20=%20" + name + "%20AND%20due<=%202d%20AND%20status%20!=%20Closed"
    url = url_link + "project%20=%20ED%20AND%20'Doc Owner'%20=%20"+name + "%20AND%20assignee%20!=%20" + name +"%20AND%20status%20!=%20Closed"

    # url = "https://automationanywhere.atlassian.net/rest/api/3/search?jql=project%20=%20ED%20AND%20'Doc Owner'%20=%20ishaan.agrawal%20AND%20due<=%202d%20AND%20status%20!=%20Closed"
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    data = json.loads(response.text)
    issues_pending = []
    print "issues_pending =", data["total"]

    for issue in data["issues"]:
        issues_pending.append(tuple((issue["key"], issue["fields"]["duedate"], issue["fields"]["status"]["name"])))

    # if data["total"] > 0:
    #     for item in issues_pending:
    #         print item[0], item[1], item[2]
    # else:
    #     print "No tickets!"

    # send_email(name, issues_pending)
    return issues_pending


# -----------------End of method----------------------

for name in list_of_recipients:

    issues_d = get_due_issues(name)
    # if len(issues_d) > 0:
    #     for item in issues_d:
    #         print item[0], item[1], item[2]
    # else:
    #     print "No tickets!"

    issues_p = get_pending_issues(name)
    # if len(issues_p) > 0:
    #     for item in issues_p:
    #         print item[0], item[1], item[2]
    # else:
    #     issues_p.append(tuple(("No ticket, eh?", "That's", "great!")))
    #     print "issues_p = ", len(issues_p)
    #     print "No tickets!"

    send_email(name, issues_d, issues_p)


# Sending mail to multiple users from Gmail account

# list of email_id to send the mail
# li = ["ishaan.agrawal@automationanywhere.com", "aditi.kashikar@automationanywhere.com"]
#
# for dest in li:
#     s = smtplib.SMTP('smtp.gmail.com', 587)
#     s.starttls()
#     s.login("ish91.agrawal@gmail.com", "ishaan1991")
#     message = "Hi! This is just a test email. Sorry for spamming. PLEASE IGNORE - there will be more coming!"
#     s.sendmail("do_not_respond@automationanywhere.com", dest, message)
#     s.quit()
