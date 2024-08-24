import requests
import datetime
import os

DOMAIN = "https://trackapi.nutritionix.com"
EXERCISE_ENDPOINT = "/v2/natural/exercise"

HEADER = {
    "x-app-id": os.environ.get('NUT_APP_ID'),
    "x-app-key": os.environ.get('NUT_API_KEY')
}

PARAMS = {
    "query": input("what did you do today")
}


full_exercise_endpoint = f"{DOMAIN}{EXERCISE_ENDPOINT}"
exercise_response = requests.post(full_exercise_endpoint, headers=HEADER, json=PARAMS)

SHEET_HEADER = {
    "Authorization": f"Bearer {os.environ.get("SHEET_AUTH_TOKEN")}"
}


def AddWorkoutToSheet(exercise, duration, calories):
    today = datetime.datetime.today().strftime("%m/%d/%Y")
    time = datetime.datetime.now().strftime("%#I:%M")
    SHEET_PARAMS = {
        "workout": {
            "date": today,
            "time": time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }
    requests.post(os.environ.get("GOOGLE_SHEET_ENDPOINT"), json=SHEET_PARAMS)


for exercise in exercise_response.json()['exercises']:
    AddWorkoutToSheet(exercise=exercise['name'], duration=exercise['duration_min'], calories=exercise['nf_calories'])



