import glob
import logging
import os
import subprocess
import sys

OUTPUT_DIR = '_dist'
SCRIPT_TO_COMPILE = 'main.py'

NOINCLUDE_DLLS = [
    'win32ui.pyd',
    'win32trace.pyd',
    'vcruntime140_1.dll',
    'libcrypto-1_1.dll',
    'mfc140u.dll',
]

NUITKA_ARGS = [
    f'--output-dir={OUTPUT_DIR}',
    '--standalone',  # or --onefile
    # '--enable-plugin=',
    '--include-data-dir=Resources=Resources',
    '--noinclude-data-files=*.py',
    '--noinclude-data-files=*.pyc',
    '--noinclude-data-files=__*',
    # '--show-progress',
    *list(map(lambda _dll: f'--noinclude-dlls={_dll}', NOINCLUDE_DLLS)),
    SCRIPT_TO_COMPILE
]
print(NUITKA_ARGS)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_nuitka_path() -> str | None:
    """
    Find the path to the Nuitka executable using the 'where' command.

    Returns:
        The path to the Nuitka executable.
    """
    result = subprocess.run(['where', 'nuitka'], capture_output=True, text=True)
    if result := result.stdout.strip().split('\n')[0]:
        return result
    else:
        return "nuitka"
        # raise FileNotFoundError("Nuitka is not installed or not found in the system.")


def compile_script(script_path: str) -> None:
    """
    Compile a Python script using Nuitka.

    Args:
        script_path: Path to the script to be compiled.
    """

    subprocess.Popen(
        [get_nuitka_path(), *NUITKA_ARGS],
        stderr=sys.stderr, stdout=sys.stdout
    ).wait()
    logging.info(f"Compilation completed successfully: {script_path}")


def apply_upx(folder_path: str, upx_path: str):
    file_paths = glob.glob(f"{folder_path}/**", recursive=True)
    file_paths = [path for path in file_paths if os.path.isfile(path)]

    for i, file_path in enumerate(file_paths):
        if os.access(file_path, os.X_OK):
            subprocess.run([upx_path, "-9", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"({i + 1}/{len(file_path)}) UPX applied to: {file_path}")
        else:
            print(f"({i + 1}/{len(file_path)}) UPX NOT applied to: {file_path}")


import contextlib

if __name__ == "__main__":
    compile_script(SCRIPT_TO_COMPILE)

    dist_dir = os.path.join(OUTPUT_DIR, "main.dist")
    for dll in NOINCLUDE_DLLS:
        with contextlib.suppress(FileNotFoundError):
            os.remove(os.path.join(dist_dir, dll))

    apply_upx(dist_dir, 'upx.exe')
