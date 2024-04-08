from fastapi import FastAPI, HTTPException, Response, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId

from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_CLUSTERNAME = os.getenv("MONGODB_CLUSTERNAME")

app = FastAPI()

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address
    
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None

#URI for MongoDB
uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTERNAME}/?retryWrites=true&w=majority&appName=Library-Management"

# Initialize MongoDB client and connect to the database
client = MongoClient(uri)
db = client["LM-Database"]
students_collection = db["Students"]

# Define API endpoints
@app.post("/students", status_code=201)
async def create_student(student: Student):
    student_data = student.model_dump()
    result = students_collection.insert_one(student_data)
    return {"id": str(result.inserted_id)}

@app.get("/students", response_model=List[Student])
async def list_students(country: Optional[str] = Query(None),
                        age: Optional[int] = Query(None)):
    #print(f"Country Filter: {country}")
    #print(f"Age Filter: {age}")
    
    filter_query = {}
    if country:
        filter_query["address.country"] = country
    if age:
        filter_query["age"] = {"$gte": age}
    
    #print(f"Filter Query: {filter_query}")
    
    students = students_collection.find(filter_query)
    return list(students)


@app.get("/students/{id}", response_model=Student)
async def get_student(id: str):
    student = students_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")


@app.patch("/students/{id}")
async def update_student(id: str, student_update: StudentUpdate):    
    # Construct the update fields based on the provided parameters
    update_fields = {}
    if student_update.name:
        update_fields["name"] = student_update.name
    if student_update.age:
        update_fields["age"] = student_update.age
    if student_update.address:
        update_fields["address"] = student_update.address.model_dump()
            
    print(f"Update fields: {update_fields}")
    
    # Try to update the student record in the database
    result = students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    print(f"MongoDB update result: {result}")

    # Check if the update was successful
    if result.modified_count == 1:
        return Response(status_code=204)
    elif result.matched_count == 0:
        # No student found with the given ID
        raise HTTPException(status_code=404, detail="Student not found")
    else:
        # Something went wrong with the update operation
        raise HTTPException(status_code=500, detail="Failed to update student")



@app.delete("/students/{id}")
async def delete_student(id: str):
    result = students_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return JSONResponse(status_code=200, content={})
    else:
        raise HTTPException(status_code=404, detail="Student not found")
