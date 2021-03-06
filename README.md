# Intro

![slacklogger_main_sample](sample_images/slacklogger_sample_1.png)

`slacklogger` is a simple Python package that logs
application-level events to your Slack channels. The
package includes a function decorator, a regular 
function, and some settings to play around with. 
Here's how everything works.

# Installation

To install `slacklogger`, use pip.

```
pip install simple-slacklogger
```

# Getting Started

To start using `slacklogger` you'll need to create
a Slack app in your Workspace. This is pretty
straightforward: 

* Once you've signed up for a Slack account head 
over to the 
[Slack Apps page](https://api.slack.com/apps).
* Click on **Create New App**, name your app, and
choose your Workspace. 
* Click on the **Create App** button.
* Click on **Oauth & Permissions** in the left
sidebar.
* Add the **'chat:write.public'** Oauth Scope 
under the **Bot Token Scopes** section. This
will also add the **'chat:write'** scope.
* On the same page, at the top, click the 
**Install App to Workspace** button.
* Click **Allow** on the next screen.
* Save the generated **Bot User OAuth Access Token**.
* Head over to the [Slack homepage](https://slack.com)
and launch your workspace in your browser. 
* Head to the channel where you want your app to 
post logs, and note the path value in the URL after
the final **'/'**. It will look something like 
**D05ZAYNAASL**. Copy this as well.

Now that you have your Slack `channel_id` and 
`access_token`, you can initialize `slacklogger`.

```
import slacklogger

slacklogger.creds = {
    "channel_id": "YOUR_CHANNEL_ID",
    "access_token": "YOUR_ACCESS_TOKEN"
}
```

# Slacklogger Decorator

The `slacklogger.log` decorator wraps around any
function and runs **before** your main function.
For example:

```
@slacklogger.log(message="It works")
def my_function():
    print("Hooray, it worked!")
``` 

"It works" will be logged in your Slack channel
**before** "Hooray, it works" is printed in your
app. If you want something more granular...

# Slacklogger Function

`slacklogger.send_log` works much the same way as 
the decorator, except it doesn't automatically
extract your function's name and script path -
you can do that with an included helper function,
`my_details`, which takes the function's name as 
a parameter. 

```
from slacklogger.helpers import my_details

def new_user(name: str):
    print("Creating new user...")
    func_name, script_path = my_details(new_user) 
    slacklogger.send_log(
        message=f"Created new user: {name}",
        function_name=func_name,
        script_path=script_path
    )
``` 

Note that if your function is in a class, and you're
using the `my_details` helper function, prepend
your function's name with `self` - for example,
`my_details(self.new_user)`.

```
from slacklogger.helpers import my_details

class User:
    def __init__(self):
        pass

    def new_user(self, name: str):
        print("Creating new user...")
        func_name, script_path = my_details(self.new_user) # <= add 'self'
        slacklogger.send_log(
            message=f"Created new user: {name}",
            function_name=func_name,
            script_path=script_path
        )
``` 

# Slacklogger Options

For both the decorator and the function, 
only the `message` parameter is
required, but you can also define the `level`, any
`tags`, and the `timezone` (this defaults to UTC).

```
@slacklogger.log(
    message="My Message",
    level="info",
    tags=["#first", "#test"],
    timezone="America/New_York",
)
def my_function():
    print("Hooray, it worked!")
```

This will output something akin to the
following in your Slack:

![slacklogger_decorator_sample](sample_images/slacklogger_sample_2.png)

The regular function has the same options, along with 
`function_name` and `script_path` as we saw above.

```
def new_user(name: str):
    print("Creating new user...")
    func_name, script_path = my_details(new_user) 
    slacklogger.send_log(
        message=f"Created new user: {name}",
        level="info",
        tags=["#new_user", "#users"]
        function_name=func_name,
        script_path=script_path,
        timezone="America/New_York"
    )
```

### Settings

You can define two settings after you enter
your credentials: `date_format` and `level_colors`.
The `date_format` setting refers to how the log date and time
are displayed. The `level_colors` setting allows
you to define a `dict` of level names and their
corresponding hex color codes.

``` 
import slacklogger

slacklogger.creds = {
    "channel_id": "MY_CHANNEL_ID",
    "access_token": "MY_ACCESS_TOKEN"
}

slacklogger.settings = {
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
```

The above values are the default settings
`slacklogger` uses. 

To create your own date formatting, 
check out [this cheat sheet for `strftime`
directives](https://strftime.org/).

```
slacklogger.settings["date_format"] = "%b %d, %H:%M"
```

For `level_colors`, you can add any name and hex
color code you need to 
`slacklogger.settings["level_colors"]` - or 
overwrite the entire `dict`.

```
slacklogger.settings["level_colors"]["ntk"] = "#730073"
```

You can use [color-hex.com](color-hex.com) to choose
color hex codes for your levels. 

Using the example directly above, we can add
a new level ('ntk', or 'Nice to Know') 
to the decorator or regular function.

```
@slacklogger.log(
    message="NTK Example",
    level="ntk",
    tags=["#level", "#test"],
    timezone="America/New_York",
)
def my_function():
    print("New level acquired!")
```

You'll see an output like this:

![slacklogger_color_sample](sample_images/slacklogger_sample_3.png)

### Timezone

To change the timezone, simply change the `timezone`
parameter in either the decorator or the function.
[Check this Wiki link](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) 
for relevant timezone names.

```
def timezone_test():
    print("Testing new timezone...")
    slacklogger.send_log(
        message="Testing Timezone",
        level="debug",
        timezone="Europe/Lisbon" # <= change this
    )
```

You should see something like this using the above
code (notice that `function_name`, `script_path`, 
and `tags` are omitted, as they're all optional).

![slacklogger_timezone_sample](sample_images/slacklogger_sample_4.png)
