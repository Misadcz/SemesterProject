import pytest
import subprocess
from unittest.mock import patch, MagicMock

# --- Simulace funkce, kterou máš někde ve slide_vm_import.py nebo v core ---
# (Pokud máš už napsanou vlastní funkci na import OVA, naimportuj si ji sem. 
# Pro účely ukázky a testu funguje tato:)
def import_virtualbox_ova(ova_path):
    """Importuje stážený .ova obraz do lokálního VirtualBoxu ve Windows."""
    # Typická cesta k VBoxManage ve Windows
    vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
    
    try:
        # Spustíme příkaz pro import OVA do VirtualBoxu
        subprocess.run(
            [vboxmanage_path, 'import', ova_path], 
            check=True, 
            capture_output=True, 
            text=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
# --------------------------------------------------------------------------


@patch('subprocess.run')
def test_import_ova_success(mock_subprocess_run):
    # Simulujeme úspěšný průběh importu OVA (VBoxManage vrací 0)
    mock_subprocess_run.return_value = MagicMock(returncode=0)
    
    # Použijeme cestu k souboru z tvé stromové struktury
    test_ova_file = "libs/test.ova"
    
    # Zavoláme naši funkci
    result = import_virtualbox_ova(test_ova_file)
    
    # Funkce musí vrátit True (úspěch)
    assert result is True
    
    # KLÍČOVÉ PRO OBHAJOBU: Kontrolujeme, že Python poslal do OS přesně tento příkaz
    mock_subprocess_run.assert_called_once_with(
        [r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe", 'import', test_ova_file],
        check=True,
        capture_output=True,
        text=True
    )


@patch('subprocess.run')
def test_import_ova_failure(mock_subprocess_run):
    """
    Ověří, že aplikace nezkolabuje, když např. VirtualBox není nainstalovaný
    nebo proces selže (např. poškozený soubor).
    """
    # Nasimulujeme pád systémového procesu (např. VBoxManage vrátil chybový kód 1)
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'VBoxManage.exe')
    
    # Zkusíme importovat s vadnými daty
    result = import_virtualbox_ova("libs/rozbity_soubor.ova")
    
    # Aplikace musí chybu zachytit a vrátit False, nikoliv spadnout
    assert result is False