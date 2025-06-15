# Slack Deployment App

## Requirements

- [ngrok](https://ngrok.com/docs/getting-started/)(for local development)
- [gcloud](https://cloud.google.com/sdk/docs/install)

## Development

- create a `.env.dev` file (get the values from your slack [app](https://api.slack.com/apps))

  ```sh
  SLACK_BOT_TOKEN=<VALUE>
  SLACK_APP_TOKEN=<VALUE>
  SLACK_SIGNING_SECRET=<VALUE>
  ```

- create a python venv and install packages using uv (or pip)

  ```sh
  uv venv
  uv add -r requirements.txt
  ```

- in a terminal, run

  ```sh
  ngrok http 3000
  ```

- in another terminal, run the app

  ```sh
  functions-framework --target=slack_deployment_summary --port=3000
  ```

- to find the `request URL` (while ngrok is running)

  ```sh
  curl http://localhost:4040/api/tunnels
  ```

- update the slack [app](https://api.slack.com/apps) with the `request URL` under:

    - **Event Subscriptions**
    - **Slash Commands**
    - **Interactivity & Shortcuts**

## Deployment

- update requirements.txt (if needed)

  ```sh
  uv export -o requirements.txt --no-dev
  ```

- create an .env.yaml file in the format

  ```yml
  SLACK_BOT_TOKEN: "<VALUE>"
  SLACK_APP_TOKEN: "<VALUE>"
  SLACK_SIGNING_SECRET: "<VALUE>"
  ```

- deploy as a google cloud run function

  ```sh
  gcloud functions deploy slack-deployment-summary \
  --runtime python311 \
  --trigger-http \
  --env-vars-file=./.env.yaml \
  --allow-unauthenticated \
  --entry-point=slack_deployment_summary \
  --region=europe-west1
  ```

- `request URL` will be in the format

  ```sh
  https://YOUR_REGION-YOUR_PROJECT_ID.cloudfunctions.net/slack-deployment-summary
  ```

- update the slack [app](https://api.slack.com/apps) with the `request URL` under:

    - **Event Subscriptions**
    - **Slash Commands**
    - **Interactivity & Shortcuts**

