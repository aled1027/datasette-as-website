# Building with Mkdocs 

I'm exploring different ways to to build & host these notes.
I manage the content in obsidian vault, so it's a set of markdown files, which should make it pretty easy.

These are some things that I want to experiment with for building. 
One thing I'm not sure about is what extent I want a FOSS project or SAAS or something that will host.

- [https://www.mkdocs.org/](https://www.mkdocs.org/)
- [https://neuron.zettel.page/](https://neuron.zettel.page/)
- [https://blot.im/](https://blot.im/)
- Git Book

I'm trying to figure out to what extent I want something FOSS and/or SAAS.

## Mkdocs

I started with mkdocs and hosting on netlify.
It took less than 10 minutes to get this up and running.
And then jsut another few minutes to find a theme that I loved: the material theme. 
For the same reasons that I love Obsidian and Gitbook, I love the material theme.
It's simple, easy to navigate, and I can see the table of contents of a page.

Here's the netlify link: [https://jolly-hotteok-51853f.netlify.app/](https://jolly-hotteok-51853f.netlify.app/).


Code sample for getting started.

```bash
# Install with brew so you can make the initial directory
brew install mkdocs
cd ~/git
mkdocs new alexs_corner_mkdocs
cd alexs_corner_mkdocs

# Once inside the directory, set up a python virtual environment.
# This seems to make it easier to add themes and other plugins
poetry init
poetry add mkdocs
poetry add mkdocs-material

# Copy the files from the Obsidian vault
cp ~/git/alexs_corner/*md docs/

# Edit mkdocs.yaml with the following:
#    site_name: Alex's Corner
#    site_url: https://jolly-hotteok-51853f.netlify.app/
#    theme: material

# Run locally
poetry run mkdocs serve

# Build into a directory called /site
poetry run mkdocs build

# Copy site/ into netlify and :boom:
```

### Mkdocs Themes

Themes: [https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes).

## Exciting Things to try
1. Build with github actions and automatically deploy to netlify
	- This could be done on the obsidian vault. The only config file


## Edit 1
I'm not sure if mkdocs is working going to work well as a blog. 
I don't want the posts sorted alphanumerically. I tried adding the dates to blog titles as a workaround but it's pretty ugly.
I found [https://squidfunk.github.io/mkdocs-material/blog/](https://squidfunk.github.io/mkdocs-material/blog/) as an approach.