# dbCode.py
# Author: Your Name
# Helper functions for database connection and queries

import pymysql
import creds
import boto3
from boto3.dynamodb.conditions import Key

def get_dynamodb_table():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=creds.aws_region,
        aws_access_key_id=creds.aws_access_key_id,
        aws_secret_access_key=creds.aws_secret_access_key
    )
    return dynamodb.Table(creds.dynamodb_table)

def add_review(item_description, reviewer_name, rating, comment):
    table = get_dynamodb_table()
    table.put_item(Item={
        'itemDescription': item_description,
        'reviewerName': reviewer_name,
        'rating': int(rating),
        'comment': comment
    })

def get_reviews(item_description):
    table = get_dynamodb_table()
    response = table.query(
        KeyConditionExpression=Key('itemDescription').eq(item_description)
    )
    return response['Items']

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def execute_insert(query, args=()):
    """Executes an INSERT/UPDATE/DELETE query and commits."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()
    