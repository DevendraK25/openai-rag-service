# sources/loader.py
import yaml
from sources.local import LocalSource
from sources.azure_blob import AzureBlobSource
import os

def load_sources(config_path="/config/sources.yaml"):
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    sources = []
    for s in cfg["sources"]:
        if s["type"] == "local":
            sources.append(LocalSource(s["path"]))
        elif s["type"] == "azure_blob":
            sources.append(AzureBlobSource(
                connection_string=s.get("connection_string"),
                container=s["container"],
                prefix=s.get("prefix", "")
            ))
        # add more types here
    return sources
