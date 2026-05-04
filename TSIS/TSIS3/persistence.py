import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_settings():
    default_settings = {
        "sound": True,
        "car_color": "Red",
        "difficulty": "Normal",
        "last_username": "Player1"
    }
    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)
        return default_settings
    
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except:
        return default_settings

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            scores = json.load(f)
            # Sort by score descending
            return sorted(scores, key=lambda x: x.get('score', 0), reverse=True)[:10]
    except:
        return []

def save_score(name, score, distance):
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": distance})
    board = sorted(board, key=lambda x: x.get('score', 0), reverse=True)[:10]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(board, f, indent=4)