import os
import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler


import sheets as sh

load_dotenv()

app = Flask(__name__)


def send_email():
    sender_email = "uiuc.schooldigest@gmail.com"
    receiver_email = "dbkeene.tsyc@gmail.com"
    password = os.getenv("GMAIL_PWD")

    message = MIMEMultipart("alternative")
    message["Subject"] = f"{datetime.datetime.now().strftime('%m/%d/%y')} UIUC Digest"
    message["From"] = sender_email
    message["To"] = receiver_email

    def get_bulk_records():
        client = sh.get_gsheet_client(os.getenv("PATH_TO_CLIENT_SECRET"))
        sheet = sh.get_google_sheet(client)

        assignments = sh.get_records(sheet, "Assignment")
        quizzes = sh.get_records(sheet, "Quiz")
        exams = sh.get_records(sheet, "Exam")
        reminders = sh.get_records(sheet, "Reminder")

        return [assignments, quizzes, exams, reminders]

    def format_records(record: list):
        html_str = ""
        for r in record:
            if r["Complete"] == "x":
                html_str += f"""
                    <del>
                        <b> {r['Course Code']} </b> - {r['Name']} ({r['Due Date']})<br>
                    </del>
                """
            else:
                html_str += f"""
                    <b> {r['Course Code']} </b> - {r['Name']} ({r['Due Date']})<br>
                """
        return html_str

    records = get_bulk_records()
    # Create the plain-text and HTML version of your message
    html = f"""\
    <html>
    <body>
        <p>Hi <b>Davis</b>,<br>
        <p>Here's your email digest for the week!<p>

            <h2 style="font-weight: bold;">
                Assignments
            </h2>

            {format_records(records[0]) or "No assignments due this week."}

            <h2 style="font-weight: bold;">
                Quizzes / Exams
            </h2>

            {format_records(records[1]) or "No quizzes for this week."}
            <br>
            {format_records(records[2]) or "No exams for this week."}

            <h2 style="font-weight: bold;">
                Reminders
            </h2>

            {format_records(records[3]) or "No reminders for this week."}
        </p>
    </body>
    </html>
    """

    # Un-comment to see HTML before it's sent
    # print(html)

    # Turn these into plain/html MIMEText objects
    html = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(html)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # Need to adjust time of day based on where PythonAnywhere server is located.
    # 9:00 AM CDT => 3:00 AM
    # So, the time here will be adjusted to hour=15
    job = scheduler.add_job(send_email, "cron", day_of_week="mon-sun", hour=15, minute=0)
    scheduler.start()
    app.run(host="0.0.0.0")
