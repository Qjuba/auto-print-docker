import pytest

from app.files import clean_original_name, stored_path


def test_original_filename_drops_path_components():
    assert clean_original_name("../../sekret/raport.pdf") == "raport.pdf"
    assert clean_original_name(r"C:\temp\raport.pdf") == "raport.pdf"


def test_stored_path_rejects_arbitrary_name():
    with pytest.raises(ValueError):
        stored_path("../../etc/passwd")


def test_stored_path_stays_in_upload_directory():
    path = stored_path("a" * 32 + ".pdf")
    assert path.parent.name == "uploads"
