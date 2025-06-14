import logging
import os

# import requests
from slack_bolt import App

# from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))
logging.basicConfig(level=logging.DEBUG)


@app.message("hello")
def message_hello(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{message['user']}>!",
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


@app.command("/summary")
def command_summary(body, ack, say, logger, client, command):
    ack()
    logger.debug(body)
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "summary-modal",
            "private_metadata": command["channel_id"],
            "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "title": {"type": "plain_text", "text": "Deployment Summary", "emoji": True},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "athena_updated_text_input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "athena_updated_text_input-action",
                        "placeholder": {"type": "plain_text", "text": "KYCCentral Dev"},
                    },
                    "label": {"type": "plain_text", "text": "Athena updated", "emoji": True},
                },
                {
                    "type": "input",
                    "block_id": "from_version_text_input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "from_version_text_input-action",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "vX.X.X",
                        },
                    },
                    "label": {"type": "plain_text", "text": "From version", "emoji": True},
                },
                {
                    "type": "input",
                    "block_id": "to_version_text_input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "to_version_text_input-action",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "vX.X.X",
                        },
                    },
                    "label": {"type": "plain_text", "text": "To version", "emoji": True},
                },
                {"type": "divider"},
                {
                    "type": "input",
                    "block_id": "migrations_text_input",
                    "element": {
                        "type": "rich_text_input",
                        "action_id": "migrations_text_input-action",
                        "initial_value": {
                            "type": "rich_text",
                            "elements": [
                                {"type": "rich_text_section", "elements": [{"type": "text", "text": "None"}]}
                            ],
                        },
                    },
                    "label": {"type": "plain_text", "text": "Migrations", "emoji": True},
                },
                {
                    "type": "input",
                    "block_id": "pip_installs_text_input",
                    "element": {
                        "type": "rich_text_input",
                        "action_id": "pip_installs_text_input-action",
                        "initial_value": {
                            "type": "rich_text",
                            "elements": [
                                {"type": "rich_text_section", "elements": [{"type": "text", "text": "None"}]}
                            ],
                        },
                    },
                    "label": {"type": "plain_text", "text": "Pip installs", "emoji": True},
                },
                {
                    "type": "input",
                    "block_id": "other_notes_text_input",
                    "element": {
                        "type": "rich_text_input",
                        "action_id": "other_notes_text_input-action",
                        "initial_value": {
                            "type": "rich_text",
                            "elements": [
                                {"type": "rich_text_section", "elements": [{"type": "text", "text": "None"}]}
                            ],
                        },
                    },
                    "label": {"type": "plain_text", "text": "Other notes", "emoji": True},
                },
                {"type": "divider"},
                {
                    "type": "input",
                    "block_id": "release_note_file_input",
                    "label": {"type": "plain_text", "text": "Upload Release Notes"},
                    "element": {
                        "type": "file_input",
                        "action_id": "release_note_file_input_action",
                        "filetypes": ["pdf"],
                        "max_files": 1,
                    },
                },
            ],
        },
    )


@app.view("summary-modal")
def handle_summary_submission(ack, body, logger, client):
    ack()
    logger.debug(body)
    channel_id = body["view"]["private_metadata"]
    state_values = body["view"]["state"]["values"]
    athena_updated = state_values["athena_updated_text_input"]["athena_updated_text_input-action"]["value"]
    from_ver = state_values["from_version_text_input"]["from_version_text_input-action"]["value"]
    to_ver = state_values["to_version_text_input"]["to_version_text_input-action"]["value"]
    migrations = state_values["migrations_text_input"]["migrations_text_input-action"]["rich_text_value"]
    pip_install = state_values["pip_installs_text_input"]["pip_installs_text_input-action"]["rich_text_value"]
    other_notes = state_values["other_notes_text_input"]["other_notes_text_input-action"]["rich_text_value"]
    release_notes = state_values["release_note_file_input"]["release_note_file_input_action"]["files"][0]
    logger.debug(f"\n{from_ver}\n {to_ver}\n {migrations}")

    # res = requests.get(
    #     release_notes["url_private"],
    #     headers={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"},
    # )
    # file_bytes = res.content
    #
    # client.files_upload_v2(
    #     channel=channel_id,
    #     title=release_notes["name"],
    #     filename=release_notes["name"],
    #     file=file_bytes,
    # )

    client.chat_postMessage(
        channel=channel_id,
        # text=f"Release notes <{release_notes['permalink']}|{release_notes['name']}>",
        blocks=[
            {
                "type": "header",
                "text": {"type": "plain_text", "text": ":owl:  Athena Deployment  :owl:"},
            },
            {
                "type": "context",
                "elements": [{"text": f"*{athena_updated}*  |  {from_ver} to {to_ver}", "type": "mrkdwn"}],
            },
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Migrations:*"}},
            migrations,
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Python packages installed:*"}},
            pip_install,
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Other notes:*"}},
            other_notes,
            {"type": "divider"},
            # {
            #     "type": "context",
            #     "elements": [
            #         {"type": "mrkdwn", "text": f"<{release_notes['permalink']}|{release_notes['name']}>"}
            #     ],
            # },
        ],
        attachments=[
            {
                "color": "#c80d0d",
                "blocks": [
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": "*Release notes:*"},
                            {
                                "type": "mrkdwn",
                                "text": f"<{release_notes['permalink']}|{release_notes['name']}>",
                            },
                        ],
                    },
                ],
            }
        ],
    )


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
