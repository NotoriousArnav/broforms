from pymongo import MongoClient
import os


con = MongoClient(
    os.getenv(
        "MONGO_URL",
        "mongodb://127.0.0.1:27017"
    )
)
db = con[
    os.getenv(
        'MONGO_DB_NAME',
        "broforms"
    )
]
