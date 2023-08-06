import speedtest
import sys
import csv
import calendar
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

print("Internet speed test has started...")

# create output folder
data_output_folder_path = "./data/"
Path(data_output_folder_path).mkdir(parents=True, exist_ok=True) 

# create speedtest object ready to receive test results
try:
    s = speedtest.Speedtest(secure=True)
except speedtest.ConfigRetrievalError as e:
    print("Didn't work. Check you're connected to the internet. If it's not that see error message for more details.")
    print()
    print("Error message: " + str(e))
    sys.exit()

# [Carry out speed test]

s.download()
s.upload()
# Extra optional code -> print(s.results.share()) # this will send my results to speedtest.net API to create a png image of my results, to which a link will be provided. Can find in results_dict also.  

# Print out speed test results
print("Download speed = " + str(round(s.results.download/1000/1000,2)) +  " Mbps") 

print("Upload speed = " + str(round(s.results.upload/1000/1000,2)) +  " Mbps")

# Create dictionary of results
results_dict = s.results.dict()

# [Extract results]

download_speed = round(results_dict["download"]/1000/1000,2) 
upload_speed = round(results_dict["upload"]/1000/1000,2)
ping = results_dict["ping"]
server_url = results_dict["server"]["url"]
server_country = results_dict["server"]["country"]
ISO_timestamp = results_dict["timestamp"]
bytes_sent = results_dict["bytes_sent"]
bytes_received = results_dict["bytes_received"]
# optional_online_png_image_of_test = results_dict["share"]
client_ISP = results_dict["client"]["isp"] 
client_IP_address = results_dict["client"]["ip"]

# [Transform timestamp]

ISO_timestamp_minus_Z = ISO_timestamp[:-1]

# convert string of timestamp into datetime object
datetimeobj = datetime.fromisoformat(ISO_timestamp_minus_Z)

# Make it aware that it's a UTC timezone.
UTC = ZoneInfo("UTC")
datetimeobj_utc = datetimeobj.replace(tzinfo=UTC)

# convert time to local timezone.
datetimeobj_local = datetimeobj.astimezone()

# extracting different datetime units to create columns.
date = str(datetimeobj_local.date())
year = datetimeobj_local.year
month = datetimeobj_local.month
month_name = calendar.month_name[datetimeobj_local.month]
day = datetimeobj_local.day
day_of_week_name = calendar.day_name[datetimeobj_local.weekday()]
time_inc_ms = datetimeobj_local.time()
time = datetimeobj_local.strftime("%H:%M:%S")
hours = datetimeobj_local.hour
minutes = datetimeobj_local.minute
seconds = datetimeobj_local.second

# [Load data into a CSV] 

# put all variables into a list in header order
results_ls = [
datetimeobj_utc.isoformat(),
datetimeobj_local.isoformat(),
date,
year,
month,
month_name,
day,
day_of_week_name,
time,
hours,
minutes,
seconds,
download_speed,
upload_speed,
ping,
server_url,
server_country,
bytes_sent,
bytes_received,
client_ISP,
client_IP_address,
]

# create daily results file
file_name = str(datetimeobj_local.date().strftime("%Y%m%d")) + "_speedtests" # e.g. 20201227_speedtests

file_path_obj = Path(data_output_folder_path + file_name + ".csv")
Absolute_file_path = str(file_path_obj.resolve())

# name headers
csv_columns = ["UTC Timestamp","Local Timestamp","Date","Year","Month","Month Name","Day","Day Name","Time","Hour","Minute","Second","Download (Mbps)","Upload (Mbps)","Ping","Server Url","Server Country","Bytes Sent","Bytes Received","My ISP","My IP Adress"] #rm share and client cols and added more cols for day and time info.

# check if file exists, if it does then append data, if not, create file, insert col headers then results.
if file_path_obj.exists(): 

    with open(str(file_path_obj), "a", newline='') as f:
        writer = csv.writer(f) # newline arg because adds extra space otherwise
        
        #insert speedtest results
        writer.writerow(results_ls) 
    
    print("Interent speed test results have been appended to file: " + Absolute_file_path)
else:

    with open(str(file_path_obj), "w", newline='') as f:
        writer = csv.writer(f)
        #insert col headers
        writer.writerow(csv_columns)
        #insert speedtest results
        writer.writerow(results_ls) 

    print("Today's first internet speed test's results have been stored in file: " + Absolute_file_path)
