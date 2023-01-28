import matplotlib.pyplot as plt
import csv
from matplotlib import dates
from datetime import date
import datetime as dt
Names = []
Values = []
today = date.today()
print("Today's date:", today)
s = str(today)

def get_seconds(time_str):
    print('Time in hh:mm:ss:', time_str)
    # split in hh, mm, ss
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

with open('Weatherdata.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    values2 = []
    for c, row in enumerate(lines):
        if s in row[0]:
            Values = row[1:-1]
            for val in Values:
                sp = val.split("|")
                for x in range(20):
                    secs = get_seconds(sp[0])
                    hms = dt.timedelta(seconds=secs+x)
                    Names.append(str(hms))
                    values2.append(sp[1])

fig, ax = plt.subplots()

ax.plot_date(Names, values2, color = 'g', linestyle = 'dashed',
         marker = 'o',label = "Weather Data")
#ax.plot_date(time, values, marker='', linestyle='-')

fig.autofmt_xdate()
#ax = plt.axes() 
#ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%b'))
#ax.xaxis.set_major_locator(dates.DayLocator(interval = 3))

#plt.scatter(Names, values2, color = 'g',s = 100)
#plt.xticks(range(10), rotation='vertical')
plt.xlabel('Names')
plt.ylabel('Values')
plt.title('Patients Blood Pressure Report', fontsize = 20)



plt.show()







# import matplotlib.pyplot as plt
# import csv
  
# x = []
# y = []
  
# with open('Weatherdata.csv','r') as csvfile:
#     lines = csv.reader(csvfile, delimiter=',')
#     for row in lines:
#         x.append(row[0])
#         y.append(int(row[1]))
  
# plt.plot(x, y, color = 'g', linestyle = 'dashed',
#          marker = 'o',label = "Weather Data")
  
# plt.xticks(rotation = 25)
# plt.xlabel('Dates')
# plt.ylabel('Temperature(°C)')
# plt.title('Weather Report', fontsize = 20)
# plt.grid()
# plt.legend()
# plt.show()