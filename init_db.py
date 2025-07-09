#!/usr/bin/env python3
"""
Initialize MongoDB with sample data
"""
from pymongo import MongoClient

def main():
    # MongoDB connection
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mergington_school"]
    activities_collection = db["activities"]
    
    print("Connecting to MongoDB...")
    
    # Clear existing data
    activities_collection.delete_many({})
    print("Cleared existing data")
    
    # Sample activities data
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
        print(f"Inserted: {activity_name}")
    
    print("Database initialized successfully!")
    print(f"Total activities: {activities_collection.count_documents({})}")
    
    # List all collections
    print("Collections:", db.list_collection_names())

if __name__ == "__main__":
    main()
