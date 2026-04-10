# [Project One Store]

**CS178: Cloud and Database Systems — Project #1**
**Author:** [Reys Aden]
**GitHub:** [ReysAden]

---

## Overview

Project One Store  inventory management system built with Flask and hosted on AWS. It allows users to add, update, delete, and view inventory items stored in a MySQL relational database. It also supports product reviews stored in DynamoDB, allowing customers to leave feedback on items.

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py                     # Main Flask application — routes and app logic
├── dbCode.py                       # Database helper functions (MySQL + DynamoDB)
├── creds_sample.py                 # Sample credentials file
├── templates/
│   ├── home.html                   # Landing page with navigation buttons
│   ├── add_inventory_item.html     # Form to add a new inventory item
│   ├── delete_inventory.html       # Form to delete an inventory item
│   ├── update_inventory.html       # Form to update an inventory item
│   ├── display_inventory.html      # Table displaying all inventory items
│   ├── display_inventory_join.html # Table displaying inventory with category names
│   ├── add_review.html             # Form to add a product review
│   └── view_reviews.html           # Page to search and view product reviews
├── .gitignore                      # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://ec2-54-146-168-28.compute-1.amazonaws.com:8080/view-reviews
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)


The relational database contains two tables:

- `Inventory` — stores inventory items; primary key is `ID` (auto-incremented); attributes are `description`, `price`, and `categoryID`
- `Category` — stores category names; primary key is `categoryID`; attributes are `name`

`Inventory.categoryID` is a foreign key that references `Category.categoryID`.

The JOIN query used in this project joins `Inventory` and `Category` on `categoryID` to display each inventory item alongside its human-readable category name instead of just a numeric ID.


### DynamoDB

- **Table name:** `ProductReviews`
- **Partition key:** `itemDescription` (String)
- **Attributes:** `reviewerName`, `rating`, `comment`
- **Used for:** Storing customer reviews for inventory items. Users can submit a review for any item by description and look up all reviews for a given item.

---

## CRUD Operations

| Operation | Route | Description |
|-----------|-------|-------------|
| Create | `/add-inventory-item` | Adds a new item to the Inventory table |
| Read | `/display-inventory-items` | Displays all inventory items |
| Read (JOIN) | `/display-inventory-with-category` | Displays inventory items with category names via SQL JOIN |
| Update | `/update-inventory-item` | Updates description, price, and category of an existing item |
| Delete | `/delete-inventory-item` | Deletes an item from inventory by description |
| Create (DynamoDB) | `/add-review` | Adds a product review to DynamoDB |
| Read (DynamoDB) | `/view-reviews` | Retrieves all reviews for a given item from DynamoDB |
---

## Challenges and Insights

One challenge was managing credentials securely across local development and EC2. Since `creds.py` is excluded from GitHub via `.gitignore`, it had to be manually configured on the EC2 instance separately from the GitHub deployment pipeline.

Setting up DynamoDB required creating a dedicated IAM user (`ProjectOneUser`) with `AmazonDynamoDBFullAccess` permissions and using its access keys in the app via boto3. This was a good introduction to AWS IAM and how access control works in practice.
---

## AI Assistance

Claude (Anthropic) was used to help debug connection errors between the Flask app, RDS, and DynamoDB. All fixes were reviewed and applied manually.
