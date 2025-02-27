from setuptools import setup, find_packages

with open("VERSION") as f:
    version = f.read().strip()

setup(
    name="magic8ball",
    version=version,
    packages=find_packages(),
    install_requires=["colorama>=0.4.0"],
    entry_points={
        'console_scripts': ['magic8ball=magic8ball:main']
    }
)
