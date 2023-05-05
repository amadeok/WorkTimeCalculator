import win32gui, pyautogui, threading,msvcrt, win32process, psutil
import time, os, sys


from playsound import playsound
from dateutil import tz

import pytz
from datetime import timezone
import datetime as dt
from enum import Enum

# class syntax
class Rec_type():
    BY_WIN_NAME = 1
    BY_PATH = 2

class entry():
    def __init__(self, window_name, rec_tpye) -> None:
        self.window_name = window_name
        self.rec_type = rec_tpye

class main:
    def __init__(self) -> None:

        self.w=win32gui
        self.time_working = 0
        self.time_working_precise = 0
        self.start_time = dt.datetime.now(pytz.timezone('Europe/Rome'))
        self.window_names = [entry("Studio One", Rec_type.BY_WIN_NAME), entry("Chrome SxS", Rec_type.BY_PATH), entry("MidiEditor -", Rec_type.BY_WIN_NAME) ]
        self.window_names.append(entry("MuseScore 3:", Rec_type.BY_WIN_NAME))
        self.window_names.append(entry("- Midi Sheet Music", Rec_type.BY_WIN_NAME))
        self.window_names.append(entry("Resolve.exe", Rec_type.BY_PATH))

        self.today = None
        self.midnight_time = None

        self.datetime_rome = self.get_today()
        print(self.datetime_rome)
        print("Today's date:", self.today)
        print("Midnight time: ", str(self.midnight_time))
        self.test = False
        self.count =  0
        self.end_time = self.start_time
        self.foreground_change = False
        self.loop_time = 1

        self.fore_win = self.w.GetForegroundWindow()
        self.prev_fore_win = self.fore_win
        self.bWorking = False

        # while 1:
        #     self.fore_win = self.w.GetForegroundWindow()
        #     if self.fore_win != 0:
        #         threadid,pid = win32process.GetWindowThreadProcessId(self.fore_win)
        #         print(self.w.GetWindowText(self.fore_win), " ", pid, " ", psutil.Process(pid).exe() ) 
        #     time.sleep(1)
            
    def get_path_from_hwd(self, hwd):
        try:
            if hwd != 0:
                threadid,pid = win32process.GetWindowThreadProcessId(hwd)
                return psutil.Process(pid).exe() 
                #print(self.w.GetWindowText(self.fore_win), " ", pid, " ", psutil.Process(pid).exe() ) 
            else:
                return ""
        except: 
            return ""

    def get_today(self):
        NYC = pytz.timezone('Europe/Rome')

        self.datetime_rome =  dt.datetime.now(NYC)
        self.today = self.datetime_rome.date()
        self.str_today = str(self.today)
        self.midnight_time = NYC.localize(dt.datetime.combine(self.datetime_rome, dt.time(hour=23, minute=59, second=57)))

        return self.datetime_rome

        
    def read_file(self, get_time_working, write_to_file=True):
        todays_line = 0

        self.datetime_rome = self.get_today()

        if not os.path.isfile("records.txt"):
            f = open("records.txt", "w+")
            f.close()

        f = open("records.txt", "r")
        data = f.readlines()

        today_registered = True

        for n, line in enumerate(data):
            line_splitted = line.split("|")
            if self.str_today in line_splitted[0]:
                if get_time_working:
                    self.time_working = float(line_splitted[2].replace("\n", ""))
                    self.time_working_precise = float(line_splitted[3].replace("\n", ""))
                todays_line = n
                today_registered = False
                break

        #self.time_working = 0 if today_registered else self.time_working
        #self.time_working_precise = 0 if today_registered else self.time_working_precise

        todays_updated = f"{str(self.today)} | {dt.timedelta(seconds=self.time_working)} | {self.time_working} | {self.time_working_precise}\n"
        if not today_registered:
            data[todays_line] = todays_updated
        else:
            data.append(todays_updated)

        f.close()

        if write_to_file:
            f = open("records.txt", "w")
            for line_ in data:
                if line_ != "\n":
                    if line_[-1] != "\n":
                        line_ += "\n"
                    f.write(line_)

            f.close()

    def write_for_visualizer(self, new_str ):
        self.datetime_rome = self.get_today()

        if not os.path.isdir("vis"):
            os.mkdir("vis")


        filename = f"vis//{self.today}.csv"
        if not os.path.isfile(filename):
            f = open(filename, "w+")
            f.close()

        f = open(filename, "a")
        f.write(new_str)
        f.close()


    def update_file(self, ):

        self.count += self.loop_time
        if self.count % 10  == 0:
            self.read_file(False)
            print("updating file ", self.count)

    def are_any_in_fore(self, handle):
        text_to_search = ""
        for entry in self.window_names:

            if entry.rec_type == Rec_type.BY_WIN_NAME:
                text_to_search = self.w.GetWindowText(handle)
            else:
                text_to_search = self.get_path_from_hwd(handle)

            if entry.window_name in text_to_search:
                return True
        return False

    def is_win_in_fore(self, fore_win):
        
        if self.are_any_in_fore(fore_win):
            return fore_win
        else:
            try:
                if fore_win != 0:  
                    h2 = self.w.GetParent(fore_win)
                    if self.are_any_in_fore(h2):
                        return h2
            except Exception as e:
                try: 
                    print(e, self.w.GetWindowText(fore_win)) 
                except Exception as e2:
                    print(e, "  ||||||||||   \n", e2)
        return None
        


    def get_seconds(self, time_str):
        hh, mm, ss = time_str.split(':')
        return int(hh) * 3600 + int(mm) * 60 + int(ss)

    def end_events(self, prev_fore_win, fore_win):

        end_time =  dt.datetime.now(pytz.timezone('Europe/Rome'))
        st = self.start_time.strftime("%H:%M:%S")
        et = end_time.strftime("%H:%M:%S")
        print("**END. start: ", st, " end ", et, "\n**prev:",self.w.GetWindowText(prev_fore_win) ,  " cur: ", self.w.GetWindowText(fore_win))

        new_str = f"{st}|{et}," #17:38:31|1$18:00:31|0,
        self.write_for_visualizer(new_str)
        delta = (end_time - self.start_time)
        self.time_working_precise += delta.total_seconds()
        self.read_file(False)
        print("updating file ", self.count)
        self.count = 0
        self.bWorking = False

    def start_events(self, prev_fore_win, fore_win):
        if self.is_win_in_fore(fore_win) and self.is_win_in_fore(prev_fore_win):
            pass
        elif not self.bWorking:
            self.start_time = dt.datetime.now(pytz.timezone('Europe/Rome'))
            print("START ", str(self.start_time))
            if self.bWorking:
                print("ERROR DOUBLE START || curr ", self.w.GetWindowText (fore_win), " || prev ", self.prev_fore_text)
                playsound("b0.mp3")
                #pyautogui.alert('ERROR DOUBLE START')
                
            self.bWorking = True

    def main_loop(self):
        while 1:
            self.prev_fore_win = self.fore_win
            self.fore_win = self.w.GetForegroundWindow()
            self.prev_fore_text = self.w.GetWindowText(self.prev_fore_win)
            #prev_fore_parent_text = self.w.GetWindowText(self.w.GetParent(self.prev_fore_win))
            # print(self.w.GetWindowText(fore_win))
            # time.sleep(0.5)
            # continue
            prev_today = self.today
            self.datetime_rome = self.get_today()
            now = dt.datetime.now(pytz.timezone('Europe/Rome'))

            delta = (self.midnight_time - now).total_seconds()
            #print("delta ", delta, str(self.midnight_time), " ", str(now))

            if abs(delta) < 2 or self.test:
                print("NEW DAY, delta: ", delta) #str(prev_today), " today: ", str(self.today)
                if self.bWorking:
                    self.end_events(self.prev_fore_win, self.fore_win)

                    print("sleeping 7 seconds")
                    time.sleep(7)

                    self.start_time = dt.datetime.now(pytz.timezone('Europe/Rome'))
                    print("START ", str(self.start_time))
                    self.time_working_precise = 0
                    self.time_working = 0

                    self.bWorking = True
                    self.test = False
                    continue

            win = self.is_win_in_fore(self.fore_win)
            if win:
                self.time_working += self.loop_time
                print("| ", f"{str(self.today)} | {dt.timedelta(seconds=self.time_working)} | ",  self.w.GetWindowText (win))
                self.update_file()
            
            if self.prev_fore_win != self.fore_win:
                if self.is_win_in_fore(self.fore_win):
                    self.start_events(self.prev_fore_win, self.fore_win)

                elif self.is_win_in_fore(self.prev_fore_win) and not self.is_win_in_fore(self.fore_win):
                    self.end_events(self.prev_fore_win, self.fore_win)

            time.sleep(self.loop_time)

def check_key_presses(m):
    x = 0
    global test
    while 1:  # ESC
        x = msvcrt.getch().decode('UTF-8')
        if x == 'q':
            sys.exit()
        elif x == 't': 
            time.sleep(7)
            print("TESTING")
            m.test = True
            m.bWorking = True

m = main()

thread = threading.Thread(target=check_key_presses, args=(m, ))
thread.start()

m.read_file(True, write_to_file=False)
m.main_loop()



  


