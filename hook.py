import configparser

import discord
import requests
from teamtalk import teamtalk


class Listener:
    def __init__(self):
        self.setup_config()
        session = requests.Session()
        self.webhook = discord.webhook.SyncWebhook.from_url(
            self.webhook_url, session=session)
        self.users = {}
        self.server = teamtalk.TeamTalkServer(self.host, self.port)
        self.server.subscribe("loggedin", self.user_join)
        self.server.subscribe("loggedout", self.user_leave)
        self.server.subscribe("adduser", self.user_join_chan)
        self.server.subscribe("removeuser", self.user_leave_chan)
        self.server.subscribe("messagedeliver", self.message)
        self.server.connect()
        self.server.login(self.nickname, self.username,
                          self.password, self.client_name)
        self.server.handle_messages()

    def setup_config(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.webhook_url = config["discord"]["webhook_url"]
        self.host = config["teamtalk"]["host"]
        self.port = config["teamtalk"]["port"]
        self.username = config["teamtalk"]["username"]
        self.password = config["teamtalk"]["password"]
        self.nickname = config["teamtalk"]["nickname"]
        self.client_name = config["teamtalk"]["client_name"]

    def send_discord_message(self, text):
        self.webhook.send(text)

    def message(self, s, params):
        source = s.get_user(params["srcuserid"])
        if source == None:
            return
        content = params["content"].strip()
        self.send_discord_message(
            f"Channel message from {source['nickname']}: {content}")

    def user_join(self, s, params):
        source = s.get_user(params["userid"])
        if source == None:
            return
        self.users[source['userid']] = source['nickname']
        self.send_discord_message(f"{self.users[source['userid']]} logged in")

    def user_join_chan(self, s, params):
        source = s.get_user(params["userid"])
        chan = s.channels[s.get_channel(params["chanid"], True)]
        if source == None:
            return
        self.send_discord_message(
            f"{source['nickname']} joined {chan['channel']}")

    def user_leave_chan(self, s, params):
        source = s.get_user(params["userid"])
        chan = s.channels[s.get_channel(params["chanid"], True)]
        if source == None:
            return
        self.send_discord_message(
            f"{source['nickname']} left {chan['channel']}")

    def user_leave(self, s, params):
        self.send_discord_message(f"{self.users[params['userid']]} logged out")
        del self.users[params['userid']]


if __name__ == "__main__":
    listener = Listener()
