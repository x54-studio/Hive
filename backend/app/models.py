from pymongo import MongoClient

client = MongoClient("mongodb+srv://CosmicToast:kwZgKXCGRIff2XTS@clusterm0.zrr90.mongodb.net/?retryWrites=true&w=majority&readPreference=primary&appName=ClusterM0")
db = client.hive_db
users_collection = db.users
articles_collection = db.articles