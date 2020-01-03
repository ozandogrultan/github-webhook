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
    payload = json.loads(request.get_data())
    url = payload["pull_request"]["url"]
    pr_url = url.split(BASE_API_ENDPOINT)[-1]
    authorization_header = {"Authorization": f"token {GITHUB_AUTH_TOKEN}"}

    r = requests.get(BASE_API_ENDPOINT + pr_url + "/files", headers=authorization_header)
    for file_dict in r.json():
        if re.match("migrations/", file_dict["filename"]):
            requests.patch(
              BASE_API_ENDPOINT + pr_url.replace("pulls/", "issues/"),
              headers=authorization_header,
              data=json.dumps({"labels": ["has migration"]})
            )
    return "OK"
