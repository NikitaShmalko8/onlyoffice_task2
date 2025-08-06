import pytest
from main_script import parse_contacts

def test_valid_file_path(tmp_path):
    file_path = tmp_path / "contacts.csv"
    parse_contacts(str(file_path))

    assert file_path.exists()

    content = file_path.read_text(encoding="utf-8").strip()
    lines = content.splitlines()

    assert len(lines) >= 1, "Файл должен содержать хотя бы одну строку данных"

def test_invalid_file_path():
    invalid_path = 'Z:/invalid/path/contacts.csv'
    with pytest.raises(Exception):
        parse_contacts(invalid_path)

def test_invalid_file_format(tmp_path):
    wrong_file = tmp_path / "output.txt"
    with pytest.raises(ValueError, match="Неверный формат файла"):
        parse_contacts(str(wrong_file))
