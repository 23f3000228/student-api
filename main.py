from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
import os
from typing import List, Optional

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def load_students():
    """Load student data from CSV file"""
    students = []
    try:
        with open('students.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Convert studentId to integer
                student = {
                    "studentId": int(row['studentId']),
                    "class": row['class']
                }
                students.append(student)
    except FileNotFoundError:
        print("CSV file not found. Please make sure 'students.csv' exists.")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []
    
    return students

@app.get("/api")
async def get_students(classes: Optional[List[str]] = Query(None, alias="class")):
    """
    Get all students or filter by class
    """
    students_data = load_students()
    
    # Filter by classes if specified
    if classes:
        filtered_students = [
            student for student in students_data 
            if student['class'] in classes
        ]
        return {"students": filtered_students}
    
    return {"students": students_data}

@app.get("/")
async def root():
    return {"message": "Student API is running. Use /api endpoint to get student data."}

# Vercel serverless function handler
async def handler(request, context):
    return app
