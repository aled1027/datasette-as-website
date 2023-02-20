"""
Deletes posts.db:db table and then recreates it from the files in the posts directory.
"""

from typing import Any
import glob
from sqlite_utils import Database
import click

def build_db_from_directory(directory: str, database: str, table: str) -> None:
    filenames = glob.glob(f"{directory}/*.md")

    posts: list[dict[str, Any]] = []
    for i, filename in enumerate(filenames):
        with open(filename) as fh:
            contents = fh.read()

        # Escape tick marks ` because they're use in the javascript rendering
        contents = contents.replace("`", "\\`")

        # Naively grab the the title of the post
        title = contents.split("\n")[0].replace("# ", "").strip()

        post = {
            "id": i,
            "title": title,
            "body": contents,
        }

        posts.append(post)


    db = Database(database)
    db[table].drop(ignore=True)
    db[table].insert_all(posts, pk="id")


@click.command()
@click.argument("directory")
@click.argument("database")
@click.argument("table")
def build(directory: str, database: str, table: str) -> None:
    build_db_from_directory(directory, database, table)


if __name__ == "__main__":
    build()