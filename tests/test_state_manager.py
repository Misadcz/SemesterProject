import pytest
import json
import os
import sys

# cesta k projektu, aby se dal importovat StateManager z core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.state_manager import StateManager 

def test_state_manager_initialization(tmp_path):
    # Test, že se třída správně inicializuje a načítá data z JSONu 
    temp_json = tmp_path / "test_state.json"
    
    # Vytvoříme testovací JSON s nějakými daty
    manager = StateManager(state_file=str(temp_json))
    
    # Ověříme, že se načítá prázdný stav, když soubor neexistuje
    assert manager.get("progress", "current_slide_index") == 0
    assert manager.state is not None

def test_state_saving_and_loading(tmp_path):
   # Ověří, že se stav správně ukládá a načítá přes metody set() a get()
    temp_json = tmp_path / "test_state.json"
    manager = StateManager(state_file=str(temp_json))
    
    # Nastavíme nějaké hodnoty a uložíme je
    manager.set("completed_steps", "git_cloned", True)
    manager.set("progress", "current_slide_index", 3)
    
    # Vytvoříme novou instanci, která by měla načíst uložená data z JSONu
    manager_reloaded = StateManager(state_file=str(temp_json))
    
    # Ověříme, že načtená data odpovídají tomu, co jsme uložili
    assert manager_reloaded.get("completed_steps", "git_cloned") is True
    assert manager_reloaded.get("progress", "current_slide_index") == 3

def test_actual_json_file_creation(tmp_path):
    # Ověří, že se skutečně vytvoří JSON soubor a obsahuje správná data
    temp_json = tmp_path / "test_state.json"
    manager = StateManager(state_file=str(temp_json))
    
    manager.set("completed_steps", "eclipse_ready", True)
    
    # Ověříme, že soubor byl vytvořen a obsahuje správná data
    assert temp_json.exists()
    with open(temp_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Ověříme, že struktura JSONu odpovídá tomu, co jsme nastavili
    assert "completed_steps" in data
    assert data["completed_steps"]["eclipse_ready"] is True