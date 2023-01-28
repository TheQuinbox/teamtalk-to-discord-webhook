# TeamTalk to Discord Webhook

This is an extremely simple Discord webhook that dispatches TeamTalk events to a particular channel.

## Usage.

1. Create a webhook.
	1. Find the channel you want the events to be sent to.
	1. Right click on it and find "Edit Channel".
	1. Find the "Integrations" tab.
	1. Click on "Webhooks", then "New Webhook".
	1. Give it a name (this is what will display in the channel whenever it sends a message), and make sure you have the URL coppied.
	1. Click save.
1. Edit the config file with all the correct info.
	1. **Important**: Do not surround these values with quotes!
1. Create a virtual environment, and activate it.
	1. `python -m venv env`
	1. env\scripts\activate
1. Install the requirements.
	1. `pip install -r requirements.txt`
1. Run the hook.
	1. `python hook.py`

## Supported events.

The following events are currently supported. Many more can be added upon request, but these are the most common ones that I think basically everyone wants.

* User logged in.
* User joined channel
* Channel message sent.
* User left channel.
* User logged out.

## Todo.

* Make supported events customizable.
	* Maybe have a section in the config file, and a boolean for all the event types.
* Proper error handling.
