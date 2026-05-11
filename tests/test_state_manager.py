import pytest
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.state_manager import StateManager 

def test_state_manager_initialization(tmp_path):
    temp_json = tmp_path / "test_state.json"
    
    manager = StateManager(state_file=str(temp_json))
    
    assert manager.get("progress", "current_slide_index") == 0
    assert manager.state is not None

def test_state_saving_and_loading(tmp_path):
    temp_json = tmp_path / "test_state.json"
    manager = StateManager(state_file=str(temp_json))
    
    manager.set("completed_steps", "git_cloned", True)
    manager.set("progress", "current_slide_index", 3)
    
    manager_reloaded = StateManager(state_file=str(temp_json))
    
    assert manager_reloaded.get("completed_steps", "git_cloned") is True
    assert manager_reloaded.get("progress", "current_slide_index") == 3

def test_actual_json_file_creation(tmp_path):
    temp_json = tmp_path / "test_state.json"
    manager = StateManager(state_file=str(temp_json))
    
    manager.set("completed_steps", "eclipse_ready", True)
    
    assert temp_json.exists()
    with open(temp_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    assert "completed_steps" in data
    assert data["completed_steps"]["eclipse_ready"] is True