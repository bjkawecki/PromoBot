# PromoBot – Telegram Bot for Product Promotions

![image](https://img.shields.io/badge/Aiogram-2CA5E0?style=flat-square&logo=telegram&logoColor=white)
![image](https://img.shields.io/badge/Python-FFD43B?style=flat-square&logo=python&logoColor=blue)
![AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=flat-square&logo=amazons3&logoColor=white)
![image](https://img.shields.io/badge/DynamoDB-4053D6?style=flat-square&logo=Amazon%20DynamoDB&logoColor=white)
![image](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white)

<!-- ![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?logo=awslambda&logoColor=fff&style=flat-square) -->

![logo](assets/logo.png)

**PromoBot** is a modular Telegram bot built with [aiogram](https://aiogram.dev/), designed to help sellers create and manage product promotions, while offering buyers a simple and interactive shopping experience via Telegram. Admins can oversee platform activity and manage users.

## Features

- Role-based behavior: Admin, Seller, Buyer
- Sellers can create, manage, and activate promotions
- Inline keyboard navigation with callback handlers
- FSM (Finite State Machine) for multi-step input flows
- Media upload support via AWS S3
- DynamoDB for data persistence

## Project Structure

```
src/
├── database/ # DynamoDB setup & repository layer
├── handlers/ # Message & callback handlers grouped by role
├── keyboards/ # Inline and reply keyboard generation
├── messages/ # Predefined texts and message templates
├── services/ # AWS S3 and other external integrations
├── states/ # FSM state definitions per role
├── utils/
├── config.py # Global configuration & constants
├── main.py
└── middleware.py
```

## Prerequisites

- Python 3.13
- A Telegram bot token
- AWS credentials (for S3)
- DynamoDB (hosted or local)

## Usage Overview

### Seller Flow

1. Seller gets activated by an admin
2. Seller registers via the bot (FSM-guided)
3. Promo details (title, image, price) are submitted
4. Media is uploaded to AWS S3
5. Inline buttons allow promo management and sharing

### Buyer Flow

1. Explore product
2. Tap on inline buttons to see more info
3. Initiate order

### Admin Flow

1. Approve or deactivate sellers
2. Manage sellers and view promos

## Tech Stack

- aiogram – Telegram bot framework (async)
- boto3 – AWS SDK for Python
- Terraform for infrastructure
- DynamoDB – NoSQL database (via repositories)
- S3 for promo images
