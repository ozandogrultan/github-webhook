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
    This endpoint acts as a webhook to add "has_migration" label to a PR
    when a Django migration is introduced.
    """
    s = requests.Session()
    if GITHUB_AUTH_TOKEN:
        s.headers.update({"Authorization": f"token {GITHUB_AUTH_TOKEN}"})
    payload = json.loads(request.get_data())
    url = payload["pull_request"]["url"]
    pr_endpoint = url.split(BASE_API_ENDPOINT)[-1]
    pr_url = BASE_API_ENDPOINT + pr_endpoint

    pr_files_response = s.get(pr_url + "/files")
    for file_dict in pr_files_response.json():
        if "migrations/" in file_dict["filename"]:
            pr_response = s.get(pr_url)
            existing_labels = [label["name"] for label in pr_response.json()["labels"]]
            # Github API uses "issues" resource for PRs as well
            s.patch(
              BASE_API_ENDPOINT + pr_endpoint.replace("pulls/", "issues/"),
              data=json.dumps({"labels": list(set(existing_labels + ["has migration"]))})
            )
            break
    return "OK"
