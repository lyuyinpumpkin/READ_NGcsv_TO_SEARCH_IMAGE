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
        filemtime=float(os.path.getmtime(path))
        if filemtime-zero_time >= -864000:
            fname,fsuffix=os.path.splitext(path)
            if fsuffix==".csv":
                csvlist.append(path)
            elif fsuffix == ".bmp" or ".jpg":
                imagelist.append(path)
            else:
                continue
        else:
            continue
print("NG SEARCH")
NGcodes=[]
NGdatas=[]
Tiao=False
if csvlist != []:
    for csvaddress in csvlist:
        with open(csvaddress,'r')as csvfile:
            reader = csv.DictReader(csvfile)
            head = reader.fieldnames
            for row in reader:
                if row['PIECE_BARCODE'] !="":
                    if row["TRAY_POSITION"]=="19" and row['ITEM14_DATA']=='error':
                        NGcodes.append(row['PIECE_BARCODE'])
                        NGdatas.append(row)
                        T = True
                        
                    elif row["TRAY_POSITION"]=="20" and row['ITEM14_DATA']=='error':
                        if Tiao == True:
                            Tiao = False
                            continue
                        else:
                            NGcodes.append(row['PIECE_BARCODE'])
                            NGdatas.append(row)
                    elif row["TRAY_POSITION"]=="21" and row['ITEM15_DATA']=='error':
                        NGcodes.append(row['PIECE_BARCODE'])
                        NGdatas.append(row)
                        T = True
                    elif row["TRAY_POSITION"]=="22" and row['ITEM15_DATA']=='error':
                        if Tiao == True:
                            Tiao = False
                            continue
                        else:
                            NGcodes.append(row['PIECE_BARCODE'])
                            NGdatas.append(row)
                    else:
                        continue
                else:
                    continue

    with open(goalpath+'\\CSV\\'+now_time+".csv","w", newline="") as savecsv:
        writer = csv.DictWriter(savecsv,fieldnames=head)
        writer.writeheader()
        writer.writerows(NGdatas)
    print("COPY START")
    print(NGcodes)
    for imageaddress in imagelist:
        print(imageaddress)
        for NGcode in NGcodes:
            print(NGcode)
            if NGcode =="":
                continue
            elif NGcode in imageaddress:
                print("执行"+NGcode)
                print("执行"+imageaddress)
                shutil.copy(imageaddress,goalpath+"\\IMAGE")
                break
            else:
                pass
else:
    pass
print("PROGRAM COPMLETE")
