"""
Deletes posts.db:db table and then recreates it from the files in the posts directory.
"""

from typing import Any
import glob
from sqlite_utils import Database
import click
import markdown
from bs4 import BeautifulSoup
from datasette_render_markdown import render_markdown


def markdown_to_html(markdown_body: str) -> str:

    """
    Converts a string of markdown to an HTML string. The implementation
    calls render_markdown from datasette-render-markdown 
    (https://github.com/simonw/datasette-render-markdown/blob/main/datasette_render_markdown/__init__.py).

    Use github flavored markdown, as described at 
    https://github.com/simonw/datasette-render-markdown#github-flavored-markdown
    Chose to call datasette-render-markdown instead of calling the markdown
    library's markdown.markdown because of the cleaning.
    """

    # Arguments needed for github-flavored markdown
    extensions = ["mdx_gfm:GithubFlavoredMarkdownExtension"]
    extra_tags = ["hr", "br", "details", "summary", "input"]
    extra_attrs = {"input": ["type", "disabled", "checked"]}

    return str(render_markdown(markdown_body, extensions, extra_tags, extra_attrs))


def build_db_from_directory(directory: str, database: str, table: str) -> None:
    filenames = glob.glob(f"{directory}/*.md")

    posts: list[dict[str, Any]] = []
    for i, filename in enumerate(filenames):
        with open(filename) as fh:
            contents = fh.read()

        html_body = markdown_to_html(contents)

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