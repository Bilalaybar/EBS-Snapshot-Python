#!/usr/bin/python
import boto3
import datetime
import pytz

ec2 = boto3.resource('ec2')

print("\n\n AWS snapshot backups started %s" %datetime.datetime.now())

#This will take a snapshot of existing volumes

for volume in ec2.volumes.all():
    vol_id = volume.vol_id
    description = "backup-%s" %(vol_id)
    ec2.create_snapshot(VolumeId=vold_id, Description=description)

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

#This will take a snapshot of existing volumes and delete in defined retention days
for instance in instances:
    instance_name = filter(lambda tag: tag ['Key'] == 'Name', instance.tags)[0]['Value']

    for volume in ec2.volumes.filter(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance.id]}]):
        description = 'scheduled_snapshot-%s.%s-%s' % (instance_name, volume.volume_id, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

        if volume.create_snapshot(VolumeID=volume.volume_id, Description=description):
            print("Snapshot created with description [%s]" % description)

        for snapshot in volume.snapshot.all():
            retention_days = 15
            if snapshot.description.startswith('scheduled_snapshot-') and ( datetime.datetime.now().replace(tzinfo=None) - snapshot.start_time.replace(tzinfo=None)) > datetime.timedelta(days=retention_days):
                print("\n\n Deleting snapshot [%s -%s ]" % (snapshot.snapshot_id, snapshot.description)):
                snapshot.delete()

print("\n\n AWS snapshot backups completed successfully")