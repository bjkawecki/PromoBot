import subprocess

import dynamodb_local


def is_dynamodb_local_running():
    try:
        output = (
            subprocess.check_output(
                [
                    "docker",
                    "ps",
                    "--filter",
                    "ancestor=amazon/dynamodb-local",
                    "--format",
                    "{{.ID}}",
                ]
            )
            .decode()
            .strip()
        )
        return len(output) > 0
    except subprocess.CalledProcessError:
        return False


def start_dynamodb_local():
    print("Starte DynamoDB Local Container...")
    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "-p",
            "8000:8000",
            "--name",
            "dynamodb_local",
            "-v",
            "./dynamodb-local-data:/home/dynamodblocal/data",
            "amazon/dynamodb-local:latest",
        ],
        check=True,
    )
    print("DynamoDB Local gestartet.")


if __name__ == "__main__":
    if not is_dynamodb_local_running():
        start_dynamodb_local()

    else:
        print("DynamoDB Local läuft bereits.")
    dynamodb_local.create_sellers_table()
    dynamodb_local.create_buyers_table()
    dynamodb_local.create_promotions_table()
    dynamodb_local.read_schema()
