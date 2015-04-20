import smtplib
import datetime
from string import Template
from optparse import OptionParser
from email.mime.text import MIMEText

from dateutil import rrule as dateutil_rrule

EMAIL_FROM = "Mr. Meeseeks <hi@gtalug.org>"
EMAIL_TO = "GTALUG Operations <operations@gtalug.org>"

DATETIME_FORMAT = "%d %B, %Y"

MEETING_DATE = list(dateutil_rrule.rrule(
    freq=dateutil_rrule.MONTHLY,
    dtstart=datetime.datetime.now(),
    count=1,
    byweekday=(dateutil_rrule.TU),
    bysetpos=2
))[0]

OPS_MEETING_DATE = list(dateutil_rrule.rrule(
    freq=dateutil_rrule.MONTHLY,
    dtstart=datetime.datetime.now(),
    count=1,
    byweekday=(dateutil_rrule.MO),
    bysetpos=4
))[0]


def send_email(subject, body):
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    s = smtplib.SMTP('localhost')
    s.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    s.quit()


def get_body(body):
    s = Template(body)

    msg_body = s.substitute(
        meeting=MEETING_DATE.strftime(DATETIME_FORMAT),
        ops=OPS_MEETING_DATE.strftime(DATETIME_FORMAT)
    )

    return msg_body


def main(subject, body):
    msg_body = get_body(body)

    send_email(subject, msg_body)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        '-f', '--file',
        dest='filename',
        help="Email template you wish to send.",
        metavar="FILE"
    )

    (options, args) = parser.parse_args()

    subject = "I'm Mr. Meeseeks! Look at me!"

    with open(options.filename, 'r') as f:
        body = f.read()

    send_email(subject, body)
