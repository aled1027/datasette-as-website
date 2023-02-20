"""
Deletes posts.db:db table and then recreates it from the files in the posts directory.
"""

from sqlite_utils.utils import TypeTracker
from typing import Any
import yaml
import glob
from sqlite_utils import Database
import click
import markdown
from bs4 import BeautifulSoup
from datasette_render_markdown import render_markdown


def drop_metadata_section(markdown_body: str) -> str:
    metadata_marker = "---"
    if not markdown_body.startswith(metadata_marker):
        return markdown_body

    end_idx = markdown_body.find(metadata_marker, len(metadata_marker))
    return markdown_body[end_idx + len(metadata_marker):]


def parse_metadata(markdown_body: str) -> dict[str, Any]:
    metadata_marker = "---"
    if not markdown_body.startswith(metadata_marker):
        return {}

    start_idx = len(metadata_marker)
    end_idx = markdown_body.find(metadata_marker, len(metadata_marker))

    if end_idx < 0:
        raise ValueError("Unable to find end of metadata section")

    metadata_section = markdown_body[start_idx:end_idx]
    metadata = yaml.safe_load(metadata_section)
    return dict(metadata)


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

    markdown_body = drop_metadata_section(markdown_body)

    return str(render_markdown(markdown_body, extensions, extra_tags, extra_attrs))


def build_db_from_directory(directory: str, database: str, table: str) -> None:
    filenames = glob.glob(f"{directory}/*.md")

    posts: list[dict[str, Any]] = []
    for i, filename in enumerate(filenames):
        with open(filename) as fh:
            contents = fh.read()

        metadata = parse_metadata(contents)
        body = drop_metadata_section(contents)
        html_body = markdown_to_html(contents)

        if "title" not in metadata:
            # If the title isn't provided in the medata, find it in the
            # html by searching for the first h1 tag
            soup = BeautifulSoup(html_body, "html.parser")
            title_tag = soup.find("h1")
            if not title_tag:
                raise ValueError("Unable to find title")
            metadata["title"] = title_tag.text
        
        title = metadata["title"]
        tags = metadata.get("tags", [])

        post = {
            "id": i,
            "title": title,
            "raw_contents": contents,
            "body": body,
            "html_body": html_body,
            "metadata": metadata,
            "tags": tags,
        }

        posts.append(post)


    db = Database(database)
    db[table].drop(ignore=True)

    tracker = TypeTracker()
    db[table].insert_all(tracker.wrap(posts), pk="id")


@click.command()
@click.argument("directory")
@click.argument("database")
@click.argument("table")
def build(directory: str, database: str, table: str) -> None:
    build_db_from_directory(directory, database, table)


if __name__ == "__main__":
    build()