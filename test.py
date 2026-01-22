import tomllib

with open("pyproject.toml", "rb") as fb:
    config = tomllib.load(fb)
print(config)
