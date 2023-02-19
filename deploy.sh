poetry run datasette publish fly posts.db \
    --app datasette-as-website \
    --metadata metadata.json \
    --template-dir templates \
    --install "datasette-render-markdown datasette-template-sql"