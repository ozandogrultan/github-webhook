# Github Webhook

This is a very basic webhook implementation using Github API and Flask and requests library.

Currently, it's purpose is to add `has migration` label to a PR when a Django migration is added with the pull request.

## How to start

Make sure you have [Flask](https://www.palletsprojects.com/p/flask/) and [requests](https://requests.readthedocs.io/en/master/) installed.

Then, clone the project and run with:

- `flask run`

You also need to have [ngrok](https://ngrok.com/) in order to expose your local server to your Github repo.

After downloading, you can do this with:

- `ngrok http 5000`

**Note:** `5000` is the default port of Flask, if you need to change it for some reason, run ngrok with `ngrok http {YOUR_PORT_NUMBER}`

For how to add webhooks to your repositories, you can refer to the [documentation](https://developer.github.com/webhooks/creating/).

### Authentication

In order to authenticate your requests, reduce rate limiting and interact with private repositories, you need to set your `GITHUB_AUTH_TOKEN` as an environment variable. You can generate a new token [here](https://github.com/settings/tokens).