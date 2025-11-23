from setuptools import setup

APP = ['menu_bar_app.py']
DATA_FILES = ['ui']
OPTIONS = {
    'iconfile': 'bitcoin_tracker_icon.icns',
    'argv_emulation': True,
    'packages': ['rumps', 'requests'],
    'plist': {
        'CFBundleName': 'Bitbar',
        'CFBundleDisplayName': 'Bitbar',
        'CFBundleGetInfoString': 'Bitbar',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'CFBundleIdentifier': 'com.defendersoftheinternet.bitcoinmenubar',
        'CFBundleDevelopmentRegion': 'en',
        'CFBundleIconFile': 'bitcoin_tracker_icon.icns',
        'LSUIElement': True,
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
