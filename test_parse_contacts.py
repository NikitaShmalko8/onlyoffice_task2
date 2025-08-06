import pytest
from main_script import parse_contacts


def test_valid_file_path(tmp_path):
    file_path = tmp_path / "contacts.csv"
    parse_contacts(str(file_path))
    assert file_path.exists()

def test_invalid_file_path():
    invalid_path = 'Z:/invalid/path/contacts.csv'
    with pytest.raises(Exception):
        parse_contacts(invalid_path)

