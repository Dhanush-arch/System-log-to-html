#!/usr/bin/env python3
import re
import operator
import csv
with open("syslog.log") as file:
    base_pattern = r"ticky: (\w*)"
    error_pattern = r"ticky: (\w*) (\w+ ?\w+?[']?\w+ ?\w+ ?\w+ ?\w+ ?\w+ ?\w+ ?\w+ ?\w+ ?\w+) \((\w*\.?\w*)\)"
    info_pattern = r"ticky: (\w*) (\w+ ?\w+ ?\w+ ?\w+ ?\w+ ?\w+ ?\w+ ?\w+ ?\w+ ?\w+) \[#\w+\] \((\w*\.?\w*)\)"
    per_dict = {}
    err_dict = {}
    final_per_dict = {}
    final_err_dict = {}
    for line in file.readlines():
        base_result = re.search(base_pattern,line)
        if base_result is not None:
            if base_result[1] == "ERROR":
                error_result = re.search(error_pattern,line)
                if error_result is not None:
                    #print(error_result[3])
                    err_dict[error_result[2]] = err_dict.get(error_result[2],0) + 1
                    if error_result[3] not in per_dict.keys():
                        per_dict[error_result[3]] = {"INFO":0,"ERROR":1}
                    else:
                        per_dict[error_result[3]]["ERROR"] += 1  
            else:
                info_result = re.search(info_pattern,line)
                if info_result is not None:
                    if info_result[3] not in per_dict.keys():
                        per_dict[info_result[3]] = {"INFO":1,"ERROR":0}
                    else:
                        per_dict[info_result[3]]["INFO"] += 1
                        
    for item in sorted(per_dict.keys()):
        final_per_dict[item] = per_dict[item]

    
    key_list = []
    value_list = []
    for key, value in err_dict.items():
        key_list.append(key)
        value_list.append(value)

    
    for key in sorted(value_list,reverse=True):
        final_err_dict[key_list[value_list.index(key)]] = key
        

    
with open('error_messages.csv', 'w',newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Error","Count"])
    for key, value in final_err_dict.items():
       writer.writerow([key, value])
    
with open('user_statistics.csv','w',newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Username","INFO","ERROR"])
    for key, value_dict in final_per_dict.items():
        writer.writerow([key,value_dict["INFO"],value_dict["ERROR"]])  
 
