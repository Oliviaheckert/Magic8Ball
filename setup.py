# setup.py
from setuptools import setup, find_packages

setup(
    name="magic8ball",
    version="1.0.0",  # Can keep using VERSION file if preferred
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.0",
        # Don't add pytest here - keep test deps separate
    ],
    entry_points={
        'console_scripts': ['magic8ball=magic8ball:main']
    },
    python_requires=">=3.8",
)
