import csv
import os
import shutil
import winreg

def desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]

import datetime as dt
now_time = dt.datetime.now().strftime('%F_%H%M%S')
print('当前时间为：' + now_time)
import time
zero_time=time.mktime(dt.date.today().timetuple())
goalpath = os.path.join(desktop_path(),"NG_INFO_SEARCH",now_time)
foldernames = ['./CSV','./IMAGE']
for foldername in foldernames:
    os.makedirs(goalpath+foldername)
fileaddress= input("ADDRESS:")

print("PROGRAM START")
csvlist=[]
imagelist=[]
for root,dirs,files in os.walk(fileaddress):
    for file in files:
        path=os.path.join(root,file)
        fname,fsuffix=os.path.splitext(path)
        filemtime=float(os.path.getmtime(path))
        if filemtime-zero_time >= -86400:
            if fsuffix==".csv":
                csvlist.append(path)
            elif fsuffix == ".bmp" or ".jpg":
                imagelist.append(path)
            else:
                continue
        else:
            continue

print("NG SEARCH")

AVIdatas=[]
for csvaddress in csvlist:
    with open(csvaddress,'r')as csvfile:
        reader = csv.DictReader(csvfile)
        head = reader.fieldnames
        for row in reader:
            pieceCode=str(row['PIECE_BARCODE'])
            if pieceCode != "":
                AVIdatas.append(row)             

with open(goalpath+'\\CSV\\'+now_time+".csv","w", newline="") as savecsv:
    writer = csv.DictWriter(savecsv,fieldnames=head)
    writer.writeheader()
    writer.writerows(AVIdatas)
print("PROGRAM COPMLETE")

