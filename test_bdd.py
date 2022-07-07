import pymongo as pm
import User_interface.mongo_connection as mc
import pprint

# connexion à la bdd
client = mc.mongodb_connect()
#client = pm.MongoClient("mongodb://localhost:27017")
db = client.graphetarium

# connexion à la collection (ou création la première fois)
coloration = db.coloration

# préparation de contenu
color01 = {"name": "interfaceH20",
        "elem": ["OW", "OS", "Si"]}

# insertion dans la bdd
if len(coloration.find_one({"name":"interfaceH20"})) == 0 :
    color01_id = coloration.insert_one(color01).inserted_id

# récupération de données
result = coloration.find_one({"name":"interfaceH20"})
result = dict(result)
dict_color = result["elem"]
pprint.pprint(dict_color)


