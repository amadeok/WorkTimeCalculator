import win32gui
w=win32gui
import time, os
time_working = 0
start_time = time.time()
window_name = "Studio One"

import pytz
from datetime import timezone
import datetime as dt

datetime_rome = dt.datetime.now(pytz.timezone('Europe/Rome'))
#print("date: ",  datetime_rome.date(), " hour ", datetime_rome.hour,":",  datetime_rome.minute,":",  datetime_rome.second)
string_i_want= datetime_rome.strftime("%H:%M:%S")

print(datetime_rome)
today = datetime_rome.date()
print("Today's date:", today)
s = str(today)
loop_time = 0.5

filename = f"{today}.csv"
if not os.path.isfile(filename):
    f = open(filename, "w+")
    f.close()
    
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
                time_working = float(line_splitted[2].replace("\n", ""))
            todays_line = n
            today_registered = False
            break

    time_working = 0 if today_registered else time_working
    
    todays_updated = f"{str(today)} | {dt.timedelta(seconds=time_working)} | {time_working}\n"
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

def write_for_visualizer( new_str ):
    f = open(filename, "a")
    f.write(new_str)
    f.close()


def update_file():
    global count

    count += loop_time
    if count % 10  == 0:
        read_file(False)
        print("updating file ", count)


def is_win_in_fore(fore_win):
    if window_name in w.GetWindowText(fore_win):
        return fore_win
    else:
        try:  
            h2 = w.GetParent(fore_win)
            if window_name in w.GetWindowText(h2):
                return h2
        except Exception as e:
            print(e) 



    return None

read_file(True, write_to_file=False)

start_time = time.time()
end_time = start_time
foreground_change = False

fore_win = w.GetForegroundWindow()
prev_fore_win = fore_win

def get_seconds(time_str):
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

while 1:
    prev_fore_win = fore_win
    fore_win = w.GetForegroundWindow()

    win = is_win_in_fore(fore_win)
    if win:
        time_working+=loop_time
        print("| ", f"{str(today)} | {dt.timedelta(seconds=time_working)} | ",  w.GetWindowText (win))
        update_file()
    
    if prev_fore_win != fore_win:
        if window_name in w.GetWindowText(fore_win):
            start_time = dt.datetime.now(pytz.timezone('Europe/Rome'))
            print("START")

        elif window_name in w.GetWindowText(prev_fore_win) and not window_name in w.GetWindowText(fore_win):
            print("END")
            end_time =  dt.datetime.now(pytz.timezone('Europe/Rome'))
            st = start_time.strftime("%H:%M:%S")
            et = end_time.strftime("%H:%M:%S")
            new_str = f"{st}|{et}," #17:38:31|1$18:00:31|0,
            write_for_visualizer(new_str)

    #current_time = dt.datetime.now().strftime("%H:%M:%S")
    #print("Current Time =", current_time)

    time.sleep(loop_time)
