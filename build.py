import subprocess
import sys

from version import VersionBuilder


def main():
    # Создаём version.txt
    version = VersionBuilder().generate()

    print(f"Версия: {version}")

    # Собираем программу
    subprocess.run([
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--name", "DesktopStream",
        "--version-file=version.txt",
        "main.py"
    ], check=True)


if __name__ == "__main__":
    main()