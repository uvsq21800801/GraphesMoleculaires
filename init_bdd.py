import pymongo as pm
import User_interface.mongo_connection as mc

# connexion à la bdd
client = mc.mongodb_connect()
db = client.graphetarium

# connexion à la collection (ou création la première fois)
colors = db.colorations

# préparation de contenu
color = {"name": "interfaceH2O",
        "elem": ["OW", "OS", "Si"],
        "hydro": False}

# insertion dans la bdd
if colors.count_documents({"name":"interfaceH2O"}) == 0 :
    color_id = colors.insert_one(color).inserted_id
print(color_id)


