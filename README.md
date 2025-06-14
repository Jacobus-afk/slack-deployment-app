# Slack Deployment App

## Requirements

- [ngrok](https://ngrok.com/docs/getting-started/)(for local development)

## Development

in a terminal, run

```sh
ngrok http 3000
```

in another terminal, run the app

```sh
python app.py
```

to find the `request URL` (while ngrok is running)

```sh
curl http://localhost:4040/api/tunnels
```

update the slack [app](https://api.slack.com/apps) with the `request URL` under:

- **Event Subscriptions**
- **Slash Commands**
- **Interactivity & Shortcuts**
