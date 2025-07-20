import paramiko
import boto3
import xlsxwriter

# AWS & SSH connection declarations
region = 'ap-south-1'
pemKeyFile = "C:\\Users\\ShounakTodankar\\DevOps\\Projects\\mykeypair.pem"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Create Workbook & Set Worksheet Headers
workbook = xlsxwriter.Workbook('EC2_Details.xlsx')
worksheet = workbook.add_worksheet()
sheetHeaders = ['Instance Name','Instance Id','Instance State','Instance Type','Public IP','Operating System','Used Memory (In MB)']
for i in range(0,len(sheetHeaders)):
    worksheet.write(0,i,str(sheetHeaders[i]))
row = 1
col = 0

# Connect to Boto3 and Fetch Instances List
myEC2Instances = boto3.client('ec2',region_name=region).describe_instances()
ownerId = myEC2Instances['Reservations'][0]['OwnerId']
instancesList = myEC2Instances['Reservations'][0]['Instances']
instancesCount = len(instancesList)

#Iterate all Instances & Capture details in worksheet
for ec2Ins in instancesList:
    instanceName = ec2Ins['Tags'][0]['Value']
    instanceId = ec2Ins['InstanceId']
    instanceState = ec2Ins['State']['Name']
    instanceType = ec2Ins['InstanceType']
    instancePublicIp = ec2Ins['NetworkInterfaces'][0]['Association']['PublicIp']
    instanceOS = ec2Ins['PlatformDetails']
    client.connect(instancePublicIp, username='ubuntu', key_filename=pemKeyFile)
    (stdin, stdout, stderr) = client.exec_command('free | awk  \'NR==2 {print $3}\'')
    instanceUsedMemory = stdout.read()
    worksheet.write(row,col,instanceName)
    worksheet.write(row,col+1,instanceId)
    worksheet.write(row,col+2,instanceState)
    worksheet.write(row,col+3,instanceType)
    worksheet.write(row,col+4,instancePublicIp)
    worksheet.write(row,col+5,instanceOS)
    worksheet.write(row,col+6,instanceUsedMemory)
    row+=1
    col=0

workbook.close()




