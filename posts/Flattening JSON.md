

# Flattening JSON

Here's a quick script for quickly flattening json

```
import pandas as pd

data = [
    {"foo": {"bar": "val1"}},
    {"foo": {"bar": "val2"}},
    {"foo": {"bar": "val3"}},
]

df = pd.json_normalize(data)
df.to_html()
df.to_csv("out.csv")
# or df.to_json, df.to_x()
```

Use in an [online jupyter notebook](https://jupyter.org/try-jupyter/lab/) to quickly run in browser. Pandas is installed in the pyodide runtime.
