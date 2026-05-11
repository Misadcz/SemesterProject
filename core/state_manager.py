import json
import os

class StateManager:
    def __init__(self, state_file="setup_state.json"):
        self.state_file = state_file
        self.state = {
            "user": {"name": "", "email": ""},
            "paths": {"repo_root": "", "java_home": "", "liferay_home": ""},
            "completed_steps": {},
            "progress": {"current_slide_index": 0}  
        }
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    for category, values in loaded_data.items():
                        if category in self.state and isinstance(values, dict):
                            self.state[category].update(values)
            except Exception as e:
                print(f"Error loading state: {e}")

    def save_state(self):
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=4)
        except Exception as e:
            print(f"Error saving state: {e}")

    def get(self, category, key, default=None):
        return self.state.get(category, {}).get(key, default)

    def set(self, category, key, value):
        if category not in self.state:
            self.state[category] = {}
        self.state[category][key] = value
        self.save_state()