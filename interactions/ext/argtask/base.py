"The base of the extension."

from interactions.ext import Base, Version, VersionAuthor
from .task import Task

version = Version(
    version="0.1.0",
    author=VersionAuthor(
        name="Saucce",
        email="saucejullyfish@gmail.com",
    ),
)

base = Base(
    name="ArgTasks",
    version=version,
    link="",
    description="An extension to add-on vanilla Task.",
    packages="interactions.ext.argtask",
)

def setup(client):
    return Task(client)