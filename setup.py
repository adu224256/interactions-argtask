from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="interactions-argtask",
    version="0.2.2",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/interactions-py/argtask",
    author="Sauce",
    author_email="saucejullyfish@gmail.com",
    license="GNU",
    packages=["interactions.ext.argtask"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["discord-py-interactions"],
)