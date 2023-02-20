"""
Deletes posts.db:db table and then recreates it from the files in the posts directory.
"""

from typing import Any
import glob
from sqlite_utils import Database
import click
import markdown
from bs4 import BeautifulSoup


def build_db_from_directory(directory: str, database: str, table: str) -> None:
    filenames = glob.glob(f"{directory}/*.md")

    posts: list[dict[str, Any]] = []
    for i, filename in enumerate(filenames):
        with open(filename) as fh:
            contents = fh.read()

        # TODO: clean up with bleach per 
        # https://github.com/simonw/datasette-render-markdown/blob/75e13878a0c0a936bbf0848a34d5c01d18c1a654/datasette_render_markdown/__init__.py#L49
        html_body = markdown.markdown(contents, output_format="html5")

        # Find the title of the post by searching for the first h1 tag
        soup = BeautifulSoup(html_body, "html.parser")
        title_tag = soup.find("h1")
        if not title_tag:
            raise ValueError("Unable to find title")
        title = title_tag.text

        post = {
            "id": i,
            "title": title,
            "body": contents,
            "html_body": html_body,
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