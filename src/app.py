"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from pymongo import MongoClient
from typing import Dict, Any

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["mergington_school"]
activities_collection = db["activities"]

# Initialize database with sample data
def initialize_database():
    """Initialize the database with sample activities if it's empty"""
    if activities_collection.count_documents({}) == 0:
        sample_activities = {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
            },
            "Gym Class": {
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"]
            },
            # スポーツ系
            "Soccer Team": {
                "description": "Join the school soccer team and compete in local leagues",
                "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
                "max_participants": 22,
                "participants": ["alex@mergington.edu", "lucas@mergington.edu"]
            },
            "Basketball Club": {
                "description": "Practice basketball skills and participate in tournaments",
                "schedule": "Tuesdays, 5:00 PM - 6:30 PM",
                "max_participants": 15,
                "participants": ["mia@mergington.edu", "liam@mergington.edu"]
            },
            # 芸術系
            "Art Club": {
                "description": "Explore various art techniques and create your own masterpieces",
                "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                "max_participants": 18,
                "participants": ["noah@mergington.edu", "ava@mergington.edu"]
            },
            "Drama Club": {
                "description": "Act, direct, and produce plays and performances",
                "schedule": "Mondays, 4:00 PM - 5:30 PM",
                "max_participants": 20,
                "participants": ["isabella@mergington.edu", "william@mergington.edu"]
            },
            # 知的系
            "Math Olympiad": {
                "description": "Prepare for math competitions and solve challenging problems",
                "schedule": "Fridays, 2:00 PM - 3:30 PM",
                "max_participants": 16,
                "participants": ["charlotte@mergington.edu", "benjamin@mergington.edu"]
            },
            "Science Club": {
                "description": "Conduct experiments and explore scientific concepts",
                "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
                "max_participants": 14,
                "participants": ["amelia@mergington.edu", "elijah@mergington.edu"]
            }
        }
        
        # Insert activities with activity name as the key
        for activity_name, activity_data in sample_activities.items():
            activities_collection.insert_one({
                "_id": activity_name,
                **activity_data
            })
        print("Database initialized with sample activities")

# Initialize database on startup
initialize_database()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Get all activities from MongoDB"""
    activities = {}
    for activity in activities_collection.find():
        activity_name = activity["_id"]
        # Remove MongoDB's _id field from the response
        activity_data = {k: v for k, v in activity.items() if k != "_id"}
        activities[activity_name] = activity_data
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    activity = activities_collection.find_one({"_id": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Add student to activity
    activities_collection.update_one(
        {"_id": activity_name},
        {"$push": {"participants": email}}
    )
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/remove")
def remove_participant_from_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    # Validate activity exists
    activity = activities_collection.find_one({"_id": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    # Remove student from activity
    activities_collection.update_one(
        {"_id": activity_name},
        {"$pull": {"participants": email}}
    )
    return {"message": f"Removed {email} from {activity_name}"}
