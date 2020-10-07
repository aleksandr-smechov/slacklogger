creds = {}
settings = {
    "date_format": "%b %d, %Y | %H:%M:%S %Z",
    "level_colors": {
        "default": "#007300",
        "debug": "#007300",
        "info": "#0000e5",
        "warn": "#e5e500",
        "error": "#e59400",
        "fatal": "#ff0000"
    }
}


from .slacklogger import *
