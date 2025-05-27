import boto3
from botocore.exceptions import ClientError

# Verbindung zu lokalem DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",
    region_name="us-west-2",  # Dummy-Region
    aws_access_key_id="fake",  # Dummy-Keys für lokal
    aws_secret_access_key="fake",
)


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


def delete_seller_table(table_name):
    try:
        table = dynamodb.Table(table_name)
        # Prüfen ob die Tabelle existiert (z. B. über describe)
        table.load()  # Ruft die Metadaten ab – wirft Fehler, wenn nicht vorhanden
        table.delete()
        table.meta.client.get_waiter("table_not_exists").wait(TableName=table_name)
        print(f"Tabelle '{table_name}' wurde gelöscht.")
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        print(f"Tabelle '{table_name}' nicht gefunden.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print(f"Tabelle '{table_name}' nicht gefunden.")
        else:
            raise  # Andere Fehler weitergeben


if __name__ == "__main__":
    delete_seller_table("sellers")
    create_sellers_table()
