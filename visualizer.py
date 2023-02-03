import datetime as dt
import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
import csv, pytz, sys


datetime_rome = dt.datetime.now(pytz.timezone('Europe/Rome'))
string_i_want= datetime_rome.strftime("%H:%M:%S")

print(datetime_rome)
today = datetime_rome.date()
s = str(today)
n = len(sys.argv)
filename = ""

if n > 1:
    if sys.argv[1] == "yesterday":
        filename = f"vis//{today - dt.timedelta(1)}.csv"
    else:
        filename = sys.argv[1]
else:
    filename =  f"vis//{today}.csv"

seconds_divisor = 10
# Generate a series of dates (these are in matplotlib's internal date format)
dates = mdates.drange(dt.datetime(2010, 1, 1), dt.datetime(2010,1,2), 
                      dt.timedelta(seconds=seconds_divisor))
            
def get_seconds(time_str):
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

counts = np.sin(np.linspace(0, 0, dates.size))

values2 = []

# with open(filename,'r') as csvfile:
#     lines = csv.reader(csvfile, delimiter=',')
#     for c, row in enumerate(lines):
#         if s in row[0]:
#             Values = row[1:-1]
#             for val in Values:
#                 sp = val.split("|")

#                 secs = get_seconds(sp[0])//10
#                 hms = dt.timedelta(seconds=secs)
#                 values2.append([secs, sp[1]])
x = 0
delta =  0
min_val = 0
with open(filename,'r') as file:
    data = file.read()
    for seg in data.split(","):
        if not len(seg) or seg == "\n":
            continue
        sp = seg.split("|")
        st = get_seconds(sp[0])
        et = get_seconds(sp[1])
        if min_val < et:
            min_val = et
        if (et >= min_val) or 1:
            delta += (et-st)
        else:
            v = 0
        for y in range(st//seconds_divisor, et//seconds_divisor):
            counts[y] = 1
        if delta < 0:
            pass

print("total time: ", delta, " ", dt.timedelta(seconds=delta))
# while x < len(values2):
#     for y in range(values2[x][0], values2[x+1][0]):
#         counts[y] = 1
#     x+=2

fig, ax = plt.subplots()


width = np.diff(dates).min()

ax.bar(dates, counts, align='center', width=width)

ax.xaxis_date()

fig.autofmt_xdate()
fig.set_figwidth(15)
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 1))

plt.show()