import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

list_of_due_issues = []
list_of_pending_issues = []
# port = 2525
# smtp_server = "smtp.mailtrap.io"

def send_email(name, list_of_due_issues, list_of_pending_issues):
    # login = "ish91.agrawal@gmail.com"  # type you email here
    # password = "ishaan1991"  # type your password here
    # login = "ishaan.agrawal@automationanywhere.com"
    login = "prod-doc@automationanywhere.com"
    # password = "I*aa2019"
    password = "AASJ@pd123#"
    # sender_email = "do_not_respond@automationanywhere.com"
    sender_email = login
    # receiver_email = name + "@automationanywhere.com"
    receiver_email = "ishaan.agrawal@automationanywhere.com"
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

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(login, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print('Sent')
