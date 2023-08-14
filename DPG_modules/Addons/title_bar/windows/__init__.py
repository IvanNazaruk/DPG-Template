try:
    import win32mica
    from .main import set_dark_mode
except ModuleNotFoundError as e:
    import logging

    logger = logging.getLogger('DPG_modules.Addons')
    logger.warning(f"[title_bar] {e.name} is not installed")


    def set_dark_mode(flag: bool):
        pass
