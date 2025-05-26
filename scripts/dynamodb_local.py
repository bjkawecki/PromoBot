import boto3

# Verbindung zu lokalem DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",
    region_name="us-west-2",  # Dummy-Region
    aws_access_key_id="fake",  # Dummy-Keys für lokal
    aws_secret_access_key="fake",
)
dynamodb_client = boto3.client(
    "dynamodb",
    endpoint_url="http://localhost:8000",
    region_name="us-west-2",  # Dummy-Region
    aws_access_key_id="fake",  # Dummy-Keys für lokal
    aws_secret_access_key="fake",
)  # Client verwenden, nicht Resource


def read_schema():
    response = dynamodb_client.describe_table(TableName="sellers")
    key_schema = response["Table"]["KeySchema"]

    for key in key_schema:
        print(f"KeyName: {key['AttributeName']}, KeyType: {key['KeyType']}")


def delete_seller_table(table_name):
    if dynamodb.Table(table_name):
        table = dynamodb.Table(table_name)
        table.delete()
        table.meta.client.get_waiter("table_not_exists").wait(TableName=table_name)
        print(f"Tabelle '{table_name}' wurde gelöscht.")
        return
    print(f"Tabelle '{table_name}' nicht gefunden.")
    return


def create_promotions_table():
    table_name = "promotions"
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if table_name not in existing_tables:
        table = dynamodb.create_table(
            TableName="promotions",
            KeySchema=[
                {"AttributeName": "seller_id", "KeyType": "HASH"},  # Partition Key
                {"AttributeName": "promotion_id", "KeyType": "RANGE"},  # Sort Key
            ],
            AttributeDefinitions=[
                {"AttributeName": "seller_id", "AttributeType": "N"},
                {
                    "AttributeName": "promotion_id",
                    "AttributeType": "S",
                },
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.wait_until_exists()
        print(f"Tabelle '{table_name}' wurde erstellt.")
    else:
        print(f"Tabelle '{table_name}' existiert bereits.")


def create_sellers_table():
    table_name = "sellers"
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if table_name not in existing_tables:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    "AttributeName": "telegram_user_id",
                    "KeyType": "HASH",
                }  # Partition key
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "telegram_user_id",
                    "AttributeType": "N",
                }  # N = Number
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.wait_until_exists()
        print(f"Tabelle '{table_name}' wurde erstellt.")
    else:
        print(f"Tabelle '{table_name}' existiert bereits.")


def create_buyers_table():
    table_name = "buyers"
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if table_name not in existing_tables:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    "AttributeName": "telegram_user_id",
                    "KeyType": "HASH",
                }  # Partition key
            ],
            AttributeDefinitions=[
                {"AttributeName": "telegram_user_id", "AttributeType": "N"}
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.wait_until_exists()
        print(f"Tabelle '{table_name}' wurde erstellt.")
    else:
        print(f"Tabelle '{table_name}' existiert bereits.")


if __name__ == "__main__":
    # delete_seller_table("seller")
    create_sellers_table()
    create_buyers_table()
    create_promotions_table()
    read_schema()
