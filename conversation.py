import logging

logger = logging.getLogger(__name__)


class Conversation:
    def __init__(self, game, engine, xhr, version, challenge_queue):
        self.game = game
        self.engine = engine
        self.xhr = xhr
        self.version = version
        self.challengers = challenge_queue

    command_prefix = "!"

    def react(self, line, game):
        logger.info("*** {} [{}] {}: {}".format(self.game.url(), line.room, line.username, line.text.encode("utf-8")))
        if (line.text[0] == self.command_prefix):
            self.command(line, game, line.text[1:].lower())

    def command(self, line, game, cmd):
        if cmd == "commands" or cmd == "help":
            self.send_reply(line, "Supported commands: !wait, !name, !howto, !eval, !queue , !About me")
        elif cmd == "wait" and game.is_abortable():
            game.ping(60, 120)
            self.send_reply(line, "Waiting 60 seconds...")
        elif cmd == "name":
            name = game.me.name
            self.send_reply(line, "{} running {} (lichess-bot v{})".format(name, self.engine.name(), self.version))
        elif cmd == "howto":
            self.send_reply(line, "How to run your own bot: Check out 'Lichess Bot API'")
        elif cmd == "eval" and line.room == "spectator":
            stats = self.engine.get_stats()
            self.send_reply(line, ", ".join(stats))
        elif cmd == "eval":
            self.send_reply(line, "I don't tell that to my opponent, sorry.")
        elif cmd == "queue":
            if self.challengers:
                challengers = ", ".join(["@" + challenger.challenger_name for challenger in reversed(self.challengers)])
                self.send_reply(line, "Challenge queue: {}".format(challengers))
            else:
                self.send_reply(line, "No challenges queued.")
         elif cmd == "About me":
                self.send_reply(line, " Hello I am a bot made by @Soloboy4 . you can Challenge me anytime in case if the bot not work or have any prob ask @Soloboy4 by Inbox and also my V2 is going to be ready soon , When its constructed Challenge him any time")
    def command(self, line, game, cmd):
        if cmd == "How I played" or cmd == "Did i played bad":
            self.send_reply(line, "Not really you didnt played bad you played very well,  There was a few mistake on this game. Practise more and improve yourself more , I would be happy then :) )
            

    def send_reply(self, line, reply):
        self.xhr.chat(self.game.id, line.room, reply)


class ChatLine:
    def __init__(self, json):
        self.room = json.get("room")
        self.username = json.get("username")
        self.text = json.get("text")
