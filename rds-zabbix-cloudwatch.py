#req: pip3 install boto3 and install zabbix-agent for zabbix_sender: pacman -S zabbix-agent

import boto3
import datetime
import os
import re

client = boto3.client('cloudwatch')

metrics = ['CPUUtilization','ReadIOPS','WriteIOPS','DatabaseConnections','FreeStorageSpace']
db = ['instance1','instance2','instance3']

def rds_monitor(metric,instance):
    response = client.get_metric_statistics(
        Namespace='AWS/RDS',
        MetricName=metric,
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': instance
            },
        ],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=300),
        EndTime=datetime.datetime.utcnow(),
        Period=300,
        Statistics= ['Maximum']
    )
    pattern = r'(?<=\bMaximum\W: )\d*'
    result = re.findall(pattern,str(response))
    return int(result[0])

for m in metrics:
    for i in db:
        z = rds_monitor(m,i)
        commando = """zabbix_sender -z zabbix.server.your.server -s {} -k {} -o {}""".format(i,m,z)
        print(command)
        os.system(command)
