class Time:
    """Represents the time of day.
       
    attributes: hour, minute, second
    """

time1 = Time()
time1.hour = 11
time1.minute = 59
time1.second = 30

time2 = Time()
time2.hour = 10
time2.minute = 30
time2.second = 15

def print_time(time):
    print("%02d:%02d:%02d" % (time.hour, time.minute, time.second))

# print_time(time1)
# print_time(time2)

def is_after(t1, t2):
    return(time1.hour > time2.hour and time1.minute > time2.minute and time1.second > time2.second)

# print(is_after(time1, time2))

def increment(time, seconds):
    time.second += seconds % 60
    time.minute += seconds // 60

    if time.second >= 60:
        time.minute += time.second // 60
        if time.second % 60 == 0:
            time.second = 0
        else:
            time.second = time.second % 60

    if time.minute >= 60:
        time.hour += time.minute // 60
        if time.minute % 60 == 0:
            time.minute = 0
        else:
            time.minute = time.minute % 60

# increment(time1, 278)
# print_time(time1)

# chapter 16 exercises

# exercise 1
def mul_time(time, mul_num):
    new_time = Time()
    minutes, new_time.second = divmod(time.second*mul_num, 60)
    hours, new_time.minute = divmod(time.minute*mul_num, 60)
    new_time.hour, new_time.minute = divmod(new_time.minute+minutes, 60)
    new_time.hour += hours + time.hour * mul_num
    return new_time

def total_seconds(total_time):
    return total_time.hour * 360 + total_time.minute * 60 + total_time.second

def avg_pace(finish_time, dist):
    # total_time = mul_time(finish_time, dist)
    total_sec = total_seconds(finish_time)
    # print(total_sec)
    avg_time = Time()
    sec_per_mile = int(total_sec / dist) # seconds per mile
    avg_time.hour, seconds = divmod(sec_per_mile, 360)
    avg_time.minute, avg_time.second = divmod(seconds, 60)
    return avg_time

new_time = mul_time(time1, 30)
# print_time(new_time)
avg_time = avg_pace(new_time, 30)
# print_time(avg_time)

from datetime import *
from re import split

# exercise 2
def print_date():
    # print(datetime.now())
    print(datetime.now().strftime("%B %d,%Y"))
    print(datetime.now().strftime("%x"))

# print_date()

def calculate_time(days):
    num_hours = days * 24

def time_to_bday(birth_date):
    birth_date_list = split('[ ,]', birth_date)
    birth_year = int(birth_date_list[-1])
    curr_date = datetime.now().date()
    birth_month = str(datetime.strptime(birth_date_list[0], "%B")).split("-")[1]
    new_birth_date = date(datetime.now().date().year+1, int(birth_month), int(birth_date_list[1]))
    left_days = new_birth_date - curr_date 
    birth_date_time = timedelta(hours=24,minutes=0,seconds=0)
    # print(birth_date_time - datetime.now().time())
    print("In " + str(left_days.days) + " days", end="")
    print(" and %02d:%02d:%02d" % (24-datetime.now().time().hour,datetime.now().time().minute,datetime.now().time().second), end="")
    print(" time you'll be " + str(int(datetime.now().year)-birth_year+1) + "!")
    # print(str(datetime.now().year))

time_to_bday("February 11, 1999")