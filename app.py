import json
import os
import re

from flask import Flask, request
import requests

BASE_API_ENDPOINT = "https://api.github.com"
GITHUB_AUTH_TOKEN = os.environ.get("GITHUB_AUTH_TOKEN")

app = Flask(__name__)


@app.route("/github-webhook/", methods=["POST"])
def add_has_migration_label():
    """
    This resource acts as a webhook to add "has_migration" label to a PR
    when a Django migration is introduced.
    """
    s = requests.Session()
    payload = json.loads(request.get_data())
    url = payload["pull_request"]["url"]
    pr_url = url.split(BASE_API_ENDPOINT)[-1]
    if GITHUB_AUTH_TOKEN:
        s.headers.update({"Authorization": f"token {GITHUB_AUTH_TOKEN}"})

    r = s.get(BASE_API_ENDPOINT + pr_url + "/files")
    for file_dict in r.json():
        if "migrations/" in file_dict["filename"]:
            s.patch(
              BASE_API_ENDPOINT + pr_url.replace("pulls/", "issues/"),
              data=json.dumps({"labels": ["has migration"]})
            )
    return "OK"
