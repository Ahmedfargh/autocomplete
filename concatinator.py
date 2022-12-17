import pandas as pd
import os
import re
def run_throug_directory_files(current_directory):
    csv_files=[]
    folders=[]
    print(current_directory)
    for folderName,subfolders,filenames in os.walk(current_directory):
            folders+=subfolders
            if subfolders==[]:
                for filename in filenames:
                    if re.search(r".csv",filename):
                        csv_files.append(filename)
    concat_same_level(csv_files,current_directory)
    for folder in folders:
        run_throug_directory_files(current_directory+"\\"+folder)
    print(folders)
def concat_same_level(list_of_csv_files,current_working):
    pd_frames=[]
    try:
        for csv_file in list_of_csv_files:
            print(type(pd.read_csv(current_working+"\\"+csv_file)))
            pd_frames.append(pd.read_csv(current_working+"\\"+csv_file))
        result=pd.concat(pd_frames)
        result.to_csv("total.csv")
    except Exception:
            return None
current_dir=os.getcwd()
run_throug_directory_files(current_dir)