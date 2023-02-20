poetry run datasette publish fly site.db \
    --app datasette-as-website \
    --metadata metadata.yaml \
    --template-dir templates \
    --static assets:static-files \
    --install "datasette-render-markdown datasette-template-sql"