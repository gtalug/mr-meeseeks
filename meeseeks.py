import argparse
import datetime
import re
import smtplib
from base64 import b64decode
from email.mime.text import MIMEText


import frontmatter
from dateutil import rrule
from github import Github
from jinja2 import Environment, PackageLoader
from pytz import timezone

from config import Config

config = Config()
eastern = timezone(config.TIMEZONE)
now = eastern.localize(datetime.datetime.now())

env = Environment(loader=PackageLoader('meeseeks', 'templates'))


def get_ops_agenda(repo, path):
    """
    Get the Operations Agenda from GitHub.
    """
    return repo.get_file_contents(path)


def get_next_meeting():
    """
    Get the next GTALUG meeting.
    """
    return list(rrule.rrule(freq=rrule.MONTHLY, dtstart=now, count=1,
                            byweekday=(rrule.TU), bysetpos=2))[0]


def get_next_ops_meeting(repo):
    """
    Get the next GTALUG Operations meeting from GitHub.
    """
    post_regex = re.compile(r'^(?P<date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})-'
                            r'(?P<doc_type>\w+).org$')

    # Let's get the last four documents.
    docs = repo.get_dir_contents('_posts')[-4:]  # TODO: This is stupid.

    for doc in docs:
        date_str, doc_type = post_regex.match(doc.name).groups()
        date = eastern.localize(datetime.datetime.strptime(date_str + 'T19:30',
                                                           '%Y-%m-%dT%H:%M'))

        if date >= now and doc_type == 'agenda':
            return date, get_ops_agenda(repo, doc.path)


def send_email(msg):
    s = smtplib.SMTP('127.0.0.1')
    s.sendmail(config.SENDER_EMAIL, config.RECIPIENT_EMAIL, msg.as_string())
    s.quit()


def main(args):
    email_tpl = env.get_template('default.txt')

    github = Github()
    repo = github.get_repo(config.GITHUB_BOARD_REPO)

    date, doc = get_next_ops_meeting(repo)
    doc = frontmatter.loads(b64decode(doc.content).decode('utf-8'))

    # TODO: This is stupid.
    margin = datetime.timedelta(days=1)

    if not now.date() == (date - margin).date():
        return True

    context = {}

    context['meeting_date'] = get_next_meeting()
    context['ops_date'] = date
    context['ops_agenda'] = doc.content

    msg = MIMEText(email_tpl.render(context))

    msg['Subject'] = 'GTALUG Operations Meeting on {}'.format(
                                        date.strftime('%-d %B %Y at %-I:%M%p'))
    msg['From'] = config.SENDER
    msg['To'] = config.RECIPIENT

    if args.send:
        send_email(msg)
    else:
        print(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("Look at me!"
                                                  "I'm Mr. Meeseeks!"))
    parser.add_argument('--send', action='store_true')
    args = parser.parse_args()

    main(args)
