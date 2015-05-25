# Mr. Meeseeks

I'm Mr. Meeseeks! Look at me!

## Usage

This script requires [cron-last-sunday](https://github.com/xr09/cron-last-sunday) to be useful.

```crontab
30 9 * * 1 /home/myles/.bin-local/run-if-today 3 "Mon" && python /home/myles/Projects/mr-meeseeks/meeseeks.py --file=/home/myles/Projects/mr-meeseeks/one-week-before-ops.txt
30 9 * * 2 /home/myles/.bin-local/run-if-today 1 "Tue" && python /home/myles/Projects/mr-meeseeks/meeseeks.py --file=/home/myles/Projects/mr-meeseeks/one-week-before-meeting.txt
0 10 * * 1 /home/myles/.bin-local/run-if-today 4 "Mon" && python /home/myles/Projects/mr-meeseeks/meeseeks.py --file=/home/myles/Projects/mr-meeseeks/day-of-ops.txt
0 10 * * 2 /home/myles/.bin-local/run-if-today 4 "Tue" && python /home/myles/Projects/mr-meeseeks/meeseeks.py --file=/home/myles/Projects/mr-meeseeks/day-of-meeting.txt
```
