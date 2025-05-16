from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import boto3
from botocore.exceptions import ClientError
import json

def get_db_credentials(secret_name="vm/postgres", region_name="us-east-1"):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = response['SecretString']
        creds = json.loads(secret)
        return creds
    except ClientError as e:
        raise Exception(f"Unable to retrieve DB credentials: {e}")

# Get credentials from Secrets Manager
creds = get_db_credentials()

# Extract username and password
username = list(creds.keys())[0]          # 'postgres'
password = creds[username]                # 'admin'

# Construct the DATABASE_URL dynamically
DATABASE_URL = f"postgresql://{username}:{password}@54.88.116.157:5432/template1"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
