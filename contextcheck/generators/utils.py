from importlib import import_module


def import_class_from_string(path: str):
    """
    Import class from string path.

    Args:
        path (str): Path to class.

    Returns:
        class: Imported class.
    """
    try:
        module_path, class_name = path.rsplit(".", 1)
        module = import_module(module_path)
        clazz = getattr(module, class_name)
        return clazz
    except (ValueError, AttributeError, ModuleNotFoundError):
        raise ImportError(f"Could not import class from path: {path}")
