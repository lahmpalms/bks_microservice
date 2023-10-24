import motor.motor_asyncio
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_DETAILS = os.getenv("DB_URL")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.microservice_database

apikey_collection = database.get_collection("apikey_collection")
log_collection = database.get_collection("log_collection")

# helper function


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
    apikey = await apikey_collection.insert_one(apikey_data)
    new_apikey = await apikey_collection.find_one({"_id": apikey.inserted_id})
    return apikey_helper(new_apikey)


async def find_api(id: str) -> dict:
    result = await apikey_collection.find_one({"apikey": id})
    if result:
        return True
    else:
        return False


async def add_log(log_data: dict) -> dict:
    log = await log_collection.insert_one(log_data)
    new_log = await log_collection.find_one({"_id": log.inserted_id})
    return (new_log)

# # Retrieve a student with a matching ID
# async def retrieve_student(id: str) -> dict:
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         return student_helper(student)


# # Update a student with a matching ID
# async def update_student(id: str, data: dict):
#     # Return false if an empty request body is sent.
#     if len(data) < 1:
#         return False
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         updated_student = await student_collection.update_one(
#             {"_id": ObjectId(id)}, {"$set": data}
#         )
#         if updated_student:
#             return True
#         return False


# # Delete a student from the database
# async def delete_student(id: str):
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         await student_collection.delete_one({"_id": ObjectId(id)})
#         return True
