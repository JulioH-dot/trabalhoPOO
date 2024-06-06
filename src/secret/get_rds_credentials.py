import boto3
import json
from botocore.exceptions import ClientError

def get_secret():

    secret_name = "rds!db-0b56ca73-8835-4da3-98e3-350c29e8e394"
    region_name = "sa-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    
    secret_dict = json.loads(secret)
    return secret_dict
