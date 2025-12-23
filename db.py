# Import required modules
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

DB_USERNAME = quote_plus(os.getenv("DB_USERNAME"))
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))

# Database Setup
uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@dify.9bbcbl1.mongodb.net/?appName=dify"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["dify"]

# Database Connection Check
try:
    client.admin.command("ping")
    print("Connected to MongoDB")
except Exception as e:
    raise RuntimeError(f"MongoDB connection failed: {e}")

# Products
products = db["products"]
products.create_index("sku", unique=True)
products_data = [
    {
        "sku": "TSHIRT-XL-BLUE",
        "name": "Blue T-Shirt XL",
        "price": 799,
        "in_stock": True,
    },
    {
        "sku": "HOODIE-M-BLACK",
        "name": "Black Hoodie M",
        "price": 1999,
        "in_stock": False,
    },
    {
        "sku": "TSHIRT-M-PINK",
        "name": "Pink T-Shirt M",
        "price": 599,
        "in_stock": False,
    },
    {
        "sku": "TOP-S-GREEN",
        "name": "Green Top S",
        "price": 1299,
        "in_stock": True,
    }
]
for p in products_data:
    products.update_one(
        {"sku": p["sku"]}, 
        {"$setOnInsert": p}, 
        upsert=True
    )
print("Products inserted")

# Leads
leads = db["leads"]
leads.create_index("phone", unique=True)
leads_data = [
    {"name": "Tanaya Jain", "phone": "+91-9999999999", "interest": "SaaS Demo"},
    {"name": "Alice Smith", "phone": "+91-8888888888", "interest": "Digital Marketing"},
    {"name": "Bob Johnson", "phone": "+91-7777777777", "interest": "Advertising"}
]
for lead in leads_data:
    leads.update_one(
        {"phone": lead["phone"]},
        {"$setOnInsert": lead},
        upsert=True
    )
print("Leads inserted")

# Orders
orders = db["orders"]
orders.create_index("order_id", unique=True)
orders_data = [
    {"order_id": "OD232131", "customer": "Rahul Raj", "status": "Processing", "amount": 3499},
    {"order_id": "OD232132", "customer": "Karishma Singh", "status": "Shipped", "amount": 1299},
    {"order_id": "OD232133", "customer": "Kajal Shah", "status": "Cancelled", "amount": 4999}
]
for order in orders_data:
    orders.update_one(
        {"order_id": order["order_id"]},
        {"$setOnInsert": order},
        upsert=True
    )
print("Orders inserted")

# Customers
customers = db["customers"]
customers_data = [
    {"name": "Amit Sharma", "email": "amit@example.com", "lifetime_purchase": 15000, "last_active_days": 20},
    {"name": "Neha Verma", "email": "neha@example.com", "lifetime_purchase": 6000, "last_active_days": 120},
    {"name": "Ritika Kapoor", "email": "ritika@example.com", "lifetime_purchase": 22000, "last_active_days": 180},
    {"name": "Sandeep Joshi", "email": "sandeep@example.com", "lifetime_purchase": 9000, "last_active_days": 15}
]
for customer in customers_data:
    customers.update_one(
        {"email": customer["email"]},
        {"$setOnInsert": customer},
        upsert=True
    )
print("Customers inserted")

# Chat logs
chat_logs = db["chat_logs"]
chat_logs.create_index([("user_id", 1), ("timestamp", -1)])
user_id = "USR001"
chat_messages = [
    {"user_id": user_id, "message": "Hi"},
    {"user_id": user_id, "message": "I need help"},
    {"user_id": user_id, "message": "Order status?"},
    {"user_id": user_id, "message": "Thanks"}
]
for msg in chat_messages:
    chat_logs.insert_one(msg)
print("Chat logs inserted")

# Insurance Request
insurance = db["insurance_requests"]
insurance_request = {
    "request_id": "INS001",
    "name": "Rohit Mehta",
    "type": "Health",
    "status": "Submitted"
}
insurance.update_one(
    {"request_id": insurance_request["request_id"]},
    {"$setOnInsert": insurance_request},
    upsert=True
)
print("Insurance requests inserted")

# Tickets
tickets = db["tickets"]
tickets_data = [
    {"ticket_id": "TCKT1001", "subject": "Login Issue", "status": "Closed"},
    {"ticket_id": "TCKT1002", "subject": "Payment Failure", "status": "Open"},
    {"ticket_id": "TCKT1003", "subject": "Account Verification", "status": "In Progress"}
]
for ticket in tickets_data:
    tickets.update_one(
        {"ticket_id": ticket["ticket_id"]},
        {"$setOnInsert": ticket},
        upsert=True
    )
print("Tickets inserted")

print("Dummy data is inserted successfully!")