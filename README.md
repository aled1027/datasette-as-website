# datasette-as-website

```bash
sqlite-utils insert posts.db posts posts.csv --csv

datasette serve posts.db --metadata metadata.json
```

## Resources

### How-tos

- https://simonwillison.net/2020/Apr/20/self-rewriting-readme/
- https://simonwillison.net/2019/Nov/25/niche-museums/
  - [Source code on github](https://github.com/simonw/museums)

### Reference

- https://datasette.io/plugins/datasette-render-markdown
- https://github.com/simonw/datasette-render-markdown
- [Datasette custom templates](https://docs.datasette.io/en/0.32/custom_templates.html#custom-templates)
- [Datasette default templates in source code](https://github.com/simonw/datasette/blob/main/datasette/templates/index.html)
