# dump_rds_log
A tool to dump AWS RDS logs to your local filesystem.

## Configuration before using

Your should follow this instruction to set up RDS Command Line Tools on your server:
http://docs.aws.amazon.com/AmazonRDS/latest/CommandLineReference/StartCLI.html

## Usage
```Shell
usage: dump_rds_log.py [-h] [-v] rds_id log_name_pattern dump_path

Dump RDS log sequential

positional arguments:
  rds_id            RDS identifier
  log_name_pattern  Pattern used to filter log file names
  dump_path         Path your log files dump to

optional arguments:
  -h, --help        show this help message and exit
  -v, --version     show program's version number and exit
```

  

## Use in crontab

Example:
```Shell
0 0 * * * source /etc/profile; /usr/bin/python /home/slow_log_dump/dump_rds_log.py my-rds slow /home/slow_log_dump/
```

Because that Unix/Linux crontab do not load your os environment variables automatically, so you have to source your profile before you rellay execute your dumping like above code.

