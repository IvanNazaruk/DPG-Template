try:
    import win32mica
    from .main import set_dark_mode
except ModuleNotFoundError as e:
    import logging

    logger = logging.getLogger('DearPyGui_Addons')
    logger.warning(f"[title_bar] {e.name} is not installed")
