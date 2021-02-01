
import requests
from requests.auth import HTTPBasicAuth
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


auth = HTTPBasicAuth("ishaan.agrawal@automationanywhere.com", "abcd123") #replace abcd123 with your JIRA API token
headers = {"Accept": "application/json"}

# url = "https://automationanywhere.atlassian.net/rest/api/3/search?jql=fixVersion%20=%20'IQ%20Bot%2011.3.5.1'%20AND%20issuetype%20in%20(improvement,%20story,%20defect,%20task)%20AND%20('Release%20Notes%20Required'%20=%20Yes%20OR%20'Additional%20Needs'%20=%20'Release%20Note%20Needed')"

list_of_recipients = [
    "ishaan.agrawal",
    "ishaan.agrawal2" # keep adding the recipients to this list
]

def get_due_issues(name):

    url_link = 'https://automationanywhere.atlassian.net/rest/api/3/search?jql='
    url = url_link+"project%20=%20ED%20AND%20'Doc Owner'%20=%20"+name+"%20AND%20due<=%202d%20AND%20status%20!=%20Closed"

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


list_of_due_issues = []
list_of_pending_issues = []
# port = 2525
# smtp_server = "smtp.mailtrap.io"

def send_email(name, list_of_due_issues, list_of_pending_issues):

    login = "abcd@somewhere.com" # type you email here
    password = "abcdxyz" #type your password here
    # sender_email = "do_not_respond@automationanywhere.com"
    sender_email = login
    # receiver_email = name + "@automationanywhere.com"
    receiver_email = "someone@somewhere.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your due ED tickets <do-not-reply> " + name
    message["From"] = sender_email
    message["To"] = receiver_email

    # write the plain text part
    text = """\
    Hey there!
    This is just a reminder email!"""

    print "Building the HTML body..."
    # write the HTML part
    html1 = """\
    <html>
      <body>
        <p>Hey there!<br>
           Just a reminder.</p>
           <h4>Tickets due</h4>
           <p>Watch out for the ticket(s) below. They're either approaching their <strong>due dates</strong> or are
           <strong>already past it</strong>.</p>"""

    html2 = ""
    if len(list_of_due_issues) > 0:
        for item in list_of_due_issues:
            html2 = html2 + '<a href="https://automationanywhere.atlassian.net/browse/' + item[0] + '">' + \
            str(item[0]) + "</a>" + "    -    " + str(item[1]) + "    -    " + str(item[2]) + "<br>"
        # <a href="https://automationanywhere.atlassian.net/browse/"+item[0]+'">'item[0]
        # https://automationanywhere.atlassian.net/browse/ED-ticketnumber
    else:
        list_of_due_issues.append(tuple(("No tickets, eh?", " ", "Fanstatic!")))
        for item in list_of_due_issues:
            html2 = html2 + item[0] + item[1] + item[2]

    html3 = """\
    <h4>Tickets in review</h4>
    <p>You might want to <strong>follow up</strong> on these with the reviewer(s):</p>
    """
    html4 = ""
    print "list_of_pending_issues = ", len(list_of_pending_issues)

    if len(list_of_pending_issues) > 0:
        for item in list_of_pending_issues:
            html4 = html4 + '<a href="https://automationanywhere.atlassian.net/browse/' + item[0] + '">' + \
            str(item[0]) + "</a>" + "    -    " + str(item[1]) + "    -    " + str(item[2]) + "<br>"
    #         # <a href="https://automationanywhere.atlassian.net/browse/"+item[0]+'">'item[0]
    #         # https://automationanywhere.atlassian.net/browse/ED-ticketnumber
    else:
        list_of_pending_issues.append(tuple(("Hmm! ", "Looks like you're being ", "vigilant!")))
        for item in list_of_pending_issues:
            html4 = html4 + item[0] + item[1] + item[2]


    html5 = """\
        <p></p>
      </body>
    </html>
    """
    body = html1 + html2 + html3 + html4 + html5
    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(body, "html")
    message.attach(part1)
    message.attach(part2)
    print "Built the HTML body..."
    # send your email

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(login, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print('Sent')

# -----------------End of method----------------------

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

    return issues_pending


# -----------------End of method----------------------

for name in list_of_recipients:

    issues_d = get_due_issues(name)
    issues_p = get_pending_issues(name)

    send_email(name, issues_d, issues_p)

