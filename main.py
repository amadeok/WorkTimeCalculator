import win32gui
w=win32gui
import time, os
time_working = 0
start_time = time.time()
window_name = "Studio One"

from datetime import date
import datetime

today = date.today()
print("Today's date:", today)
s = str(today)

count =  0

def read_file(get_time_working, write_to_file=True):
    todays_line = 0
    global time_working
    if not os.path.isfile("records.txt"):
        f = open("records.txt", "w+")
        f.close()

    f = open("records.txt", "r")
    data = f.readlines()

    today_registered = True

    for n, line in enumerate(data):
        line_splitted = line.split("|")
        if s in line_splitted[0]:
            if get_time_working:
                time_working = int(line_splitted[2])
            todays_line = n
            today_registered = False
            break
        
    todays_updated = f"{str(today)} | {datetime.timedelta(seconds=time_working)} | {time_working}\n"
    if not today_registered:
        data[todays_line] = todays_updated
    else:
        data.append(todays_updated)

    f.close()

    if write_to_file:
        f = open("records.txt", "w")
        for line_ in data:
            if line != "\n":
                f.write(line_)

        f.close()

def update_file():
    global count
    count+=1
    if count % 10 == 0:
        read_file(False)
        print("updating file ", count)


read_file(True, write_to_file=False)

while 1:
    h = w.GetForegroundWindow()
    if window_name in w.GetWindowText(h):
        time_working+=1
        print("| ", f"{str(today)} | {datetime.timedelta(seconds=time_working)} | ",  w.GetWindowText (h))
        update_file()
    else:
        try:
            h2 = w.GetParent(h)
        except Exception as e:
            print(e) 
        if window_name in w.GetWindowText(h2):
            time_working+=1
            print("| ", f"{str(today)} | {datetime.timedelta(seconds=time_working)} | ",  w.GetWindowText (h2))
            update_file()

    #read_file(False)

    #print(w.GetWindowText (h2))

    time.sleep(1)
