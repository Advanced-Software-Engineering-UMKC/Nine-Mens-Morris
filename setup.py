from setuptools import setup, find_packages

setup(
    name='Nine-Mens-Morris',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'startgame=frontend.GameGUI:main',  # Adjust as necessary
        ],
    },
)