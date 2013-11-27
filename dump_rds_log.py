import time
import subprocess
import shlex
import re
import argparse
import os.path
import sys
from xml.etree import ElementTree

# Script arguments parser
parser = argparse.ArgumentParser(
    description='Dump RDS log sequential',
    version="0.1"
    )

parser.add_argument('rds_id', action="store", help="RDS identifier") 
parser.add_argument('log_name_pattern', action="store", help="Pattern used to filter log file names")
parser.add_argument('dump_path', action="store", help="Path your log files dump to")

arguments = parser.parse_args()
rds_id = arguments.rds_id
log_name_pattern = arguments.log_name_pattern
dump_path = arguments.dump_path.rstrip('/')
dump_log = dump_path + '/' + rds_id + "-" + log_name_pattern + ".log"
process_log = dump_path + '/' + rds_id + "-" + log_name_pattern + "-process.log"
time_file = dump_path + '/' + rds_id + "-" + log_name_pattern + ".time"

# Get rds log list
raw_cmd = "rds-describe-db-log-files %s --filename-contains %s --show-xml" % (rds_id, log_name_pattern)
cmd = shlex.split(raw_cmd)
res = subprocess.check_output(cmd)
strinfo=re.compile(' xmlns=.*')
res = strinfo.sub('>',res)
root = ElementTree.fromstring(res)
tree = ElementTree.ElementTree(root)
file_list = []
for elem in tree.iter(tag='DescribeDBLogFilesDetails'):
    single_file = []
    for child in elem:
        single_file.append(child.text)
    file_list.append(single_file)

for i in range(len(file_list)):
    for j in range(i+1, len(file_list)):
        if file_list[i][0] > file_list[j][0]:
            temp = file_list[i]
            file_list[i] = file_list[j]
            file_list[j] = temp
# Exclude crunttly been writting log file
for file in file_list:
    if file[1].endswith("log"):
        file_list.remove(file)
# Dump log
try:
    #pdb.set_trace()
    os.chdir(dump_path)
    try:
        with open(process_log, 'a') as f:
            start_time = time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
            f.write("# Start dump at %s" % start_time)
    except IOError as e:
        print e
    try:
        with open(time_file, 'r') as f:
            last_append = f.readline()
    except IOError:
        last_append = 0
    with open(dump_log, 'a') as f:
        for file in file_list:
            if file[0] > last_append:
                raw_cmd = "rds-download-db-logfile %s --log-file-name %s" % (rds_id, file[1])
                cmd = shlex.split(raw_cmd)
                res = subprocess.check_output(cmd)
                print "Dumping %s" % file
                with open(process_log, 'a') as f_process_log:
                    f_process_log.write("Dumping %s\n" % file)
                f.write(res)
                with open(time_file, 'w') as f_time_file:
                    f_time_file.write(file[0])
except OSError as e:
    print e
