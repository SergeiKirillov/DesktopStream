from datetime import datetime
from pathlib import Path

class Version:
    """Версия программы на основе даты и времени сборки."""

    FORMAT = "%Y%m%d-%H%M"

    def __init__(self, dt=None):
        self.datetime = dt or datetime.now()

    @property
    def value(self):
        return self.datetime.strftime(self.FORMAT)

    @property
    def compact(self):
        return self.datetime.strftime("%Y%m%d%H%M")

    @property
    def date(self):
        return self.datetime.strftime("%Y-%m-%d")

    @property
    def time(self):
        return self.datetime.strftime("%H:%M")

    def __str__(self):
        return self.value

class VersionBuilder:
    """
    Генерирует version.txt для PyInstaller.
    Формат версии:
        filevers=(YYYY, DDMM, 0, HHMM)
    Например:
        filevers=(2026, 2208, 0, 1023)
    """

    def __init__(self, filename="version.txt"):
        self.filename = Path(filename)

    def generate(self):
        now = datetime.now()

        year = now.year
        day_month = int(now.strftime("%d%m"))
        hours_minutes = int(now.strftime("%H%M"))

        version = f"{year}.{day_month}.{hours_minutes}"

        content = f'''# UTF-8
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=({year}, {day_month}, 0, {hours_minutes}),
        prodvers=({year}, {day_month}, 0, {hours_minutes}),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct('CompanyName', 'https://sergeikirillov.github.io/'),
                        StringStruct('FileDescription', 'Desktop to stream'),
                        StringStruct('FileVersion', '{version}'),
                        StringStruct('InternalName', 'main'),
                        StringStruct('OriginalFilename', 'main.exe'),
                        StringStruct('ProductName', 'DesktopStream'),
                        StringStruct('ProductVersion', '{version}'),
                    ]
                )
            ]
        ),
        VarFileInfo(
            [VarStruct('Translation', [1033, 1200])]
        )
    ]
)
'''

        self.filename.write_text(content, encoding="utf-8")

        return version