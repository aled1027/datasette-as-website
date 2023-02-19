# Obsidian Git

Added the obsidian git plugin so now to deploy to netlify, it's as easy as:

1. Command-p: `Obsidian Git: Create Backup`

And that command does:

1. Looks for what files changed and commits
2. Pushes to github
3. Which triggers the github action
4. The github action builds with mkdocs and pushes to netlify