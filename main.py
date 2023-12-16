import json

exercise_path = "example.json" 

if __name__ == "__main__":
    exercise_file = open(exercise_path, "r")
    print(json.loads(exercise_file.read()))
    
