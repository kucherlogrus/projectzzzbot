import os
import time

import telegram

import credentials


class TelegrammBot:

    def __init__(self):
        self.bot = telegram.Bot(token=credentials.token)
        self.last_update_id = -1
        self.delay = 10
        self.channel_name = "Project Zzzzz"
        self.workdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/zzzbot"
        self.start_time = time.time()
        self.getIdFromStorage()
        self.shutdown = False

    def run(self):
        while True:
            before_tick = time.time()
            self.tick()
            after_tick = time.time()
            elapsed = after_tick - before_tick
            time_to_wait = self.delay - elapsed
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            if self.shutdown:
                return

    def tick(self):
        updates = self._get_new_updates()
        for update in updates:
            self.handleUpdate(update)
        self._markUpdates(updates)

    def handleUpdate(self, update):
        message = update.message
        if message.text is None:
            return
        if message.chat.title == self.channel_name and message.text.startswith("/"):
            self.handleChannelCommand(message)

    def handleChannelCommand(self, message):
        command = message.text[1:]
        if command == 'sayhi':
            self.bot.send_message(chat_id=message.chat.id, text="Привет, я ZzzBot")
            return
        if command.startswith('echo '):
            name = message.from_user.first_name
            text = message.text.replace("/echo", f"{name}, написал:")
            self.bot.send_message(chat_id=message.chat.id, text=text)
            return
        if command == 'shutdown':
            self.bot.send_message(chat_id=message.chat.id, text="Выключаюсь. Пока")
            self.shutdown = True
            return
        self.bot.send_message(chat_id=message.chat.id, text="Я такой команды еще не знаю.")

    def _get_new_updates(self):
        if self.last_update_id == -1:
            return self.bot.get_updates(read_latency=50)
        return self.bot.get_updates(offset=self.last_update_id)

    def _markUpdates(self, updates: list):
        if len(updates) > 0:
            self.last_update_id = updates[-1]['update_id'] + 1
            with open(f"{self.workdir}/storage.txt", 'w') as f:
                f.write(str(self.last_update_id))

    def getIdFromStorage(self):
        try:
            with open(f"{self.workdir}/storage.txt", 'r') as f:
                str_id = f.read()
                self.last_update_id = int(str_id)
        except Exception as err:
            print(err)


if __name__ == '__main__':
    bot = TelegrammBot()
    bot.run()
