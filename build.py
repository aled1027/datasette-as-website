"""
Deletes posts.db:db table and then recreates it from the files in the posts directory.
"""

from typing import Any
import glob
from sqlite_utils import Database

filenames = glob.glob("posts/*.md")

posts: list[dict[str, Any]] = []
for i, filename in enumerate(filenames):
    with open(filename) as fh:
        contents = fh.read()

    # Escape tick marks ` because they're use in the javascript rendering
    contents = contents.replace("`", "\\`")
    print(contents)

    # Naively grab the the title of the post
    title = contents.split("\n")[0].replace("# ", "").strip()

    
    post = {
        "id": i,
        "title": title,
        "body": contents,
    }

    posts.append(post)


db = Database("posts.db")
db["posts"].drop(ignore=True)
db["posts"].insert_all(posts, pk="id")