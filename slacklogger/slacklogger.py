import os
import json
import pytz
import inspect
import requests
from functools import wraps
from datetime import datetime
from pytz import UnknownTimeZoneError


def log(
    message: str,
    level: str = "info",
    tags: list = [],
    timezone: str = "",
):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from . import creds, settings

            if "channel_id" not in creds:
                raise Exception(
                    "You need include a Slack channel ID in your creds dictionary"
                )
            elif "access_token" not in creds:
                raise Exception(
                    "You need include a Slack access token in your creds dictionary"
                )

            channel_id = creds["channel_id"]
            access_token = creds["access_token"]

            date_format = settings["date_format"]
            level_colors = settings["level_colors"]
            level_color = level_colors.get(level, "default")

            now = pytz.utc.localize(datetime.utcnow())
            if timezone:
                try:
                    now = now.astimezone(pytz.timezone(timezone))
                except UnknownTimeZoneError:
                    raise UnknownTimeZoneError(
                        """
                            You need to enter a correct 
                            timezone name, such as 'America/New_York'.
                            See this page for a complete list: 
                            https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
                        """
                    )

            function_name = f.__name__
            script_path = os.path.abspath(inspect.getfile(f))

            blocks = construct_slack_blocks(
                message,
                level,
                date_format,
                level_color,
                now,
                function_name,
                script_path,
                tags,
            )

            slack_endpoint = "https://slack.com/api/chat.postMessage"
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {
                "channel": channel_id,
                "blocks": json.dumps(blocks),
            }
            r = requests.post(slack_endpoint, headers=headers, params=params)
            print(r.text)
            return f(*args, **kwargs)

        return wrapper

    return decorator


def send_log(
    message: str,
    level: str = "info",
    tags: list = [],
    function_name: str = "",
    script_path: str = "",
    timezone: str = "",
):
    from . import creds, settings

    if "channel_id" not in creds:
        raise Exception("You need include a Slack channel ID in your creds dictionary")
    elif "access_token" not in creds:
        raise Exception(
            "You need include a Slack access token in your creds dictionary"
        )

    channel_id = creds["channel_id"]
    access_token = creds["access_token"]

    date_format = settings["date_format"]
    level_colors = settings["level_colors"]
    level_color = level_colors.get(level, "default")

    now = pytz.utc.localize(datetime.utcnow())
    if timezone:
        try:
            now = now.astimezone(pytz.timezone(timezone))
        except UnknownTimeZoneError:
            raise UnknownTimeZoneError(
                """
                    You need to enter a correct 
                    timezone name, such as 'America/New_York'.
                    See this page for a complete list: 
                    https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
                """
            )

    blocks = construct_slack_blocks(
        message, level, date_format, level_color, now, function_name, script_path, tags
    )

    slack_endpoint = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "channel": channel_id,
        "blocks": json.dumps(blocks),
    }
    r = requests.post(slack_endpoint, headers=headers, params=params)

    return r.text, r.status_code


def construct_slack_blocks(
    message: str,
    level: str,
    date_format: str,
    level_color: str,
    now: datetime,
    function_name: str,
    script_path: str,
    tags: list,
):
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"{now.strftime(date_format)}"},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{level.upper()}* \n {message}",
            },
            "accessory": {
                "type": "image",
                "image_url": f"https://htmlcolors.com/color-image/{level_color[1:].lower()}.png",
                "alt_text": f"{level_color}",
            },
        },
    ]

    if function_name:
        blocks[1]["text"]["text"] += f"\n\n _Function *{function_name}*_"
        if script_path:
            blocks[1]["text"]["text"] += f" _in *{script_path}*_"
    if tags:
        blocks.append(
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": f"*Tags:* {' '.join(tags)}"}],
            }
        )

    return blocks
