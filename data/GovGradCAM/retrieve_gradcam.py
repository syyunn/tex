import boto3
import pickle

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='AKIATHBCLRR3R7QE2W7Q',
                          aws_secret_access_key='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',
                          region_name='us-east-1'
)

table = dynamodb.Table('GovGradCAM-w7ry3boc7fcczbydbhi56dhbqm-dev')

response = table.scan()
data = response['Items']


count = 0
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    with open(f'/Users/suyeol/tex/data/GovGradCAM/download/GovGradCAM_{count}.pkl', 'wb') as f:
        items = response['Items']
        pickle.dump(items, f)
        f.close()
    print('number', count, ':', len(items), 'newly fetched')
    count += 1

if __name__ == "__main__":
    pass
