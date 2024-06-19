import pytest

SKIP_DEFAULT_FLAGS = ["ollama", "openai"]


def pytest_addoption(parser):
    for flag in SKIP_DEFAULT_FLAGS:
        parser.addoption(
            "--{}".format(flag),
            action="store_true",
            default=False,
            help="run {} tests".format(flag),
        )


def pytest_configure(config):
    for flag in SKIP_DEFAULT_FLAGS:
        config.addinivalue_line("markers", flag)


def pytest_collection_modifyitems(config, items):
    for flag in SKIP_DEFAULT_FLAGS:
        if config.getoption("--{}".format(flag)):
            continue

        skip_mark = pytest.mark.skip(reason="need --{} option to run".format(flag))
        for item in items:
            if flag in item.keywords:
                item.add_marker(skip_mark)
