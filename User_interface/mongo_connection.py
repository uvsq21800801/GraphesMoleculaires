import pymongo as pm

client_uri = "mongodb+srv://lambe:lambe@phasetest.mg7kc.mongodb.net/?retryWrites=true&w=majority"
maxSevSelDelay = 30000

def mongodb_connect():
    try:
        client = pm.MongoClient(client_uri,
                                     serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
        return client
    except pm.errors.ConnectionFailure or pm.errors.ServerSelectionTimeoutError as err:
         print("Failed to connect to server "+str(client_uri)+" : "+str(err))

