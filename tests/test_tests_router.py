from pathlib import Path

import pytest

from contextcheck.executors.tests_router import TestsRouter


def test_initialize_paths(tmp_path):
    test_file = tmp_path / "test_file.yaml"
    test_file.write_text("test content")
    test_folder = tmp_path / "test_folder"
    test_folder.mkdir()

    data = {
        "output_type": "file",
        "output_folder": str(tmp_path),
        "filename": [str(test_file)],
        "folder": str(test_folder),
    }
    router = TestsRouter(**data)

    assert isinstance(router.output_folder, Path)
    assert isinstance(router.filename[0], Path)
    assert isinstance(router.folder, Path)
    assert router.filename[0] == test_file
    assert router.folder == test_folder


def test_check_filename(tmp_path):
    valid_file = tmp_path / "valid.yaml"
    valid_file.write_text("test")

    data = {"output_type": "console", "filename": [str(valid_file)]}
    router = TestsRouter(**data)

    assert valid_file in router.filename

    # Test with an invalid file
    with pytest.raises(ValueError, match="do not exist"):
        TestsRouter(output_type="console", filename=["invalid_file.yaml"])


def test_check_folder(tmp_path):
    data = {"output_type": "console", "folder": str(tmp_path)}
    router = TestsRouter(**data)

    assert router.folder == tmp_path

    # Test with an invalid folder
    with pytest.raises(ValueError, match="does not exist"):
        TestsRouter(output_type="console", folder="invalid_folder")


def test_ensure_output_folder_exists(tmp_path):
    output_folder = tmp_path / "new_output_folder"

    data = {"output_type": "file", "output_folder": str(output_folder)}
    TestsRouter(**data)

    assert output_folder.exists()
    assert output_folder.is_dir()
