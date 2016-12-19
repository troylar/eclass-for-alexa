import boto3
import optparse
from pprint import pprint
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
client = boto3.client('dynamodb')
table_name="EClass"
does_table_exist = False
try:
   table=client.describe_table(TableName=table_name)
   print "%s table already exists" % (table_name)
   does_table_exist = True

except Exception as e:
   if "Requested resource not found: Table" in str(e):
      print "Creating %s table" % (table_name)
      table=dynamodb.create_table(
         TableName="EClass",
         KeySchema=[
            { 
               'AttributeName': 'student_id',
               'KeyType': 'HASH'
            },
            {
               'AttributeName': 'student_name',
               'KeyType': 'RANGE'
            }
         ],
         AttributeDefinitions = [
            {
               'AttributeName': 'student_id',
               'AttributeType': 'S'
            },
            {
               'AttributeName': 'student_name',
               'AttributeType': 'S'
            }
         ],
         ProvisionedThroughput={
              'ReadCapacityUnits': 1,
              'WriteCapacityUnits': 1
          }
      )
      print "Waiting for table to be ready . . ."
      table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
      print "%s table is ready" % (table_name)
      does_table_exist = True
   else:
     print "%s table cannot be created" % (table_name)
     raise
pprint(table)
quit()

print("Table status:", table.table_status)