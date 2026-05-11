import pytest
import subprocess
from unittest.mock import patch, MagicMock

from gui.slides.slide_vm_import import import_virtualbox_ova


@patch('subprocess.run')
def test_import_ova_success(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(returncode=0)
    test_ova_file = "libs/test.ova"
    
    result = import_virtualbox_ova(test_ova_file)
    
    assert result is True
    mock_subprocess_run.assert_called_once_with(
        [r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe", 'import', test_ova_file],
        check=True,
        capture_output=True,
        text=True
    )

@patch('subprocess.run')
def test_import_ova_failure_process_error(mock_subprocess_run):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'VBoxManage.exe')
    
    result = import_virtualbox_ova("libs/rozbity_soubor.ova")
    
    assert result is False

@patch('subprocess.run')
def test_import_ova_failure_not_installed(mock_subprocess_run):
    mock_subprocess_run.side_effect = FileNotFoundError()
    
    result = import_virtualbox_ova("libs/test.ova")
    
    assert result is False