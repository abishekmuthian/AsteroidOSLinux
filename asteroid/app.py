
import cmd
import colorama
import functools
import logging
import queue
import sys
import threading
from gi.repository import GLib
import paho.mqtt.client as mqtt
import asteroid
import json


class LogFormatter(logging.Formatter):

    @staticmethod
    @functools.lru_cache(10)
    def _prefix(prefix, color):
        return colorama.Style.RESET_ALL + "[" + color + prefix + \
               colorama.Style.RESET_ALL + "]"

    _namecolors = {
        "DEBUG": ("DBG", colorama.Fore.LIGHTWHITE_EX),
        "INFO": ("INF", colorama.Fore.LIGHTBLUE_EX),
        "WARNING": ("WRN", colorama.Fore.LIGHTYELLOW_EX),
        "ERROR": ("ERR", colorama.Fore.LIGHTRED_EX),
        "CRITICAL": ("CRT", colorama.Fore.LIGHTRED_EX),
        "UNKNOWN": ("???", colorama.Fore.LIGHTWHITE_EX)
    }

    def format(self, record):
        prefix = LogFormatter._prefix(
            *LogFormatter._namecolors.get(
                record.levelname,
                LogFormatter._namecolors["DEBUG"]))
        return prefix + " " + super(LogFormatter, self).format(record)


class App:

    def __init__(self, address, broker_address, mqtt_topic, cmd=True, verbose=False):
        self._setup_logging(verbose)
        self.asteroid = asteroid.Asteroid(address)
        self.loop = GLib.MainLoop()
        self.modules = []
        self._setup_mqtt(broker_address, mqtt_topic)

    def _setup_logging(self, verbose):
        syslog = logging.StreamHandler(sys.stderr)
        formatter = LogFormatter()
        syslog.setFormatter(formatter)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        self.logger.addHandler(syslog)

    def _on_message(self, client, userdata, message):
        payload = json.loads(message.payload)
        self.logger.info("message received %s", payload)
        self.logger.info("message topic= %s", message.topic)
        self.logger.info("message qos= %s", message.qos)
        self.logger.info("message retain flag= %s", message.retain)
        self.asteroid.notify(payload["summary"], body=payload["body"],
                             id_=(payload["id"] if "id" in payload else None),
                             app_name=(payload["app_name"] if "app_name" in payload else None),
                             app_icon=(payload["app_icon"] if "app_icon" in payload else None))
        self.logger.info("Battery level: %d", self.asteroid.battery_level())

    def _setup_mqtt(self, broker_address, mqtt_topic):
        self.logger.info("creating new mqtt instance")
        self.logger.info("creating new instance")
        client = mqtt.Client("P1")  # create new instance
        client.on_message = self._on_message  # attach function to callback
        self.logger.info("connecting to broker")
        client.connect(broker_address)  # connect to broker
        client.loop_start()  # start the loop
        self.logger.info("Subscribing to topic %s", mqtt_topic)
        client.subscribe("house/smartwatch")

    def run(self):
        self.logger.info("Entering GLib event loop")
        self.loop.run()

    def register_module(self, module):
        module.register(self)
        # We don't really do anything with these yet, but just in case
        self.modules.append(module)
