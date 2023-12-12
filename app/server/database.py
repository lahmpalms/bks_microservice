import motor.motor_asyncio
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import HTTPException

load_dotenv()
MONGO_DETAILS = os.getenv("DB_URL")
MONGO_DB = os.getenv("MONGO_DB")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client[MONGO_DB]

apikey_collection = database.get_collection("apikey_collection")
log_collection = database.get_collection("log_collection")
service_collection = database.get_collection("service_collection")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# helper function

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def apikey_helper(apikey) -> dict:
    return {
        "id": str(apikey["_id"]),
        "fullname": apikey["fullname"],
        "email": apikey["email"],
        "apikey": apikey["apikey"],
    }

# Retrieve all apikey present in the database


async def retrieve_apikeys():
    apikeys = []
    async for apikey in apikey_collection.find():
        apikeys.append(apikey_helper(apikey))
    if len(apikeys) == 0:
        return None
    else:
        return apikeys


async def add_apikey(apikey_data: dict) -> dict:
    payload = {'fullname': apikey_data["fullname"], 'email': apikey_data["email"],
               'password': get_password_hash(apikey_data["password"]), 'apikey': apikey_data["apikey"]}
    apikey = await apikey_collection.insert_one(payload)
    new_apikey = await apikey_collection.find_one({"_id": apikey.inserted_id})
    return apikey_helper(new_apikey)


async def find_api(id: str) -> dict:
    result = await apikey_collection.find_one({"apikey": id})
    if result:
        return True
    else:
        return False


async def check_userdata(user_data: dict) -> dict:
    result = await apikey_collection.find_one({"email": user_data.email})

    if result:
        check = True if result["email"] == user_data.email and verify_password(
            user_data.password, result["password"]) else False
        if check:
            result_data = {
                "email": result.get("email"),
                "apikey": result.get("apikey"),
            }
            return result_data
    else:
        return False


async def add_log(log_data: dict) -> dict:
    log = await log_collection.insert_one(log_data)
    new_log = await log_collection.find_one({"_id": log.inserted_id})
    return (new_log)


async def create_service(service_data: dict) -> dict:
    try:
        document = {
            "service_name": service_data.service_name,
            "apikey": service_data.apikey
        }
        result = await service_collection.insert_one(document)
        service_id = result.inserted_id
        return {"service_id": str(service_id)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating service: {str(e)}")


async def patch_service_apikey(service_id: str, apikey_update) -> dict:
    try:
        # Convert the service_id to ObjectId
        service_id_obj = ObjectId(service_id)

        # Define the update operation to only update the apikey field
        update_operation = {
            "$set": {"apikey": apikey_update.apikey}
        }

        # Perform the update operation
        result = await service_collection.update_one(
            {"_id": service_id_obj},
            update_operation
        )

        # Check if the update was successful
        if result.modified_count == 1:
            return {"message": "API key updated successfully"}
        else:
            raise HTTPException(
                status_code=404, detail="Service not found")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating API key: {str(e)}")


async def check_access_service(service_id: str, apikey_to_check: str) -> bool:
    try:
        # Convert the service_id to ObjectId
        service_id_obj = ObjectId(service_id)
        # Perform a query to find documents where the given API key is in the 'apikey' array
        cursor = service_collection.find({
            "_id": service_id_obj,
            "apikey": {"$in": [apikey_to_check]}
        })

        # Iterate over the cursor using await
        async for document in cursor:
            return True  # If there is at least one document, return True

        # If no documents were found, return False
        return False
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error checking access service: {str(e)}")
