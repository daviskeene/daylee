# School Digest

School Digest is a Flask application to send me a daily digest of assignments, quizzes, exams, and reminders within the next 7 days.

I created this project to give myself better visibility into what I have to do for school.

## About

To get assignment, exam, and quiz information, I manually scraped my course websites and entered this data into a Google Sheet.
Shortly thereafter, I made a Google Form that I can use to enter upcoming assignment or exam dates.

While the Flask app is running, at 9:00am it will download and filter all the course information that I have entered and send me
and email containing all the information I need in the next 7 days. I decided to break this data up into four categories:
- Assignments
- Quizzes
- Exams
- Reminders

## Getting Started

I will work to make this project more configurable in the future. For now, you can read the source code to see how I set everything up.
My project tree looks like the following:
```
.
├── README.md
├── client_secret.json  <- hidden, obtained from authenticating a Service Account via Google API
├── main.py
├── requirements.txt
├── sheets.py
└── .env  <- hidden, contains gmail password and path to client_secret.json
```