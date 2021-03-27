import abc
import os
import json
import struct
import socket
import threading

from google.protobuf.json_format import MessageToJson
from protocols import vssref_command_pb2

def get_config(config_file=None):
    """Return parsed config_file."""
    if config_file:
        config = json.loads(open(config_file, 'r').read())
    else:
        config = json.loads(open('config.json', 'r').read())

    return config

class RefereeComm(threading.Thread):
    
    def __init__(self):
        """The RefereeComm class creates a socket to communicate with the Referee.

        Methods:
            run(): calls _create_socket() and parses the status message from the Referee.
            can_play(): returns if game is currently on GAME_ON.
            get_status(): returns current status.
            get_color(): Returns color of the team that will kick in the penalty or goal kick.
            get_quadrant(): Returns the quandrant in which the free ball will occur.
            get_foul(): Return current foul.
            _create_socket(): returns new socket binded to the Referee.
        """
        super(RefereeComm, self).__init__()
        self.config = get_config()
        self.commands = []

        self._status = None

        self.referee_port = int(os.environ.get('REFEREE_PORT', self.config['network']['referee_port']))
        self.host = os.environ.get('REFEREE_IP', self.config['network']['referee_ip'])

        self._can_play = False
        self._color = None
        self._quadrant = None
        self._foul = None

    
    def run(self):
        """Calls _create_socket() and parses the status message from the Referee."""
        print("Starting referee...")
        self.referee_sock = self._create_socket()
        print("Referee completed!")
        while True:
            c = vssref_command_pb2.VSSRef_Command()
            data = self.referee_sock.recv(1024)
            c.ParseFromString(data)
            self._status = json.loads(MessageToJson(c))
            print(self._status)

            self._can_play = self._status.get('foul') == 'GAME_ON'
            if (self._status.get('foul') != 'GAME_ON'):
                self._foul = self._status.get('foul')
            if (self._status.get('foul') == 'FREE_BALL'):
                self._quadrant = self._status.get('foulQuadrant')
            elif (self._status.get('foul') == 'PENALTY_KICK' or self._status.get('foul') == 'GOAL_KICK'):
                self._color = self._status.get('teamcolor')

    def can_play(self):
        """Returns if game is currently on GAME_ON."""
        return self._can_play

    def get_status(self):
        """Returns current status."""
        return self._status

    def get_color(self):
        """Returns color of the team that will kick in the penalty or goal kick."""
        return self._color
    
    def get_quadrant(self):
        """Returns the quandrant in which the free ball will occur."""
        return self._quadrant
    
    def get_foul(self):
        """Return current foul."""
        return self._foul

    def _create_socket(self):
        """Returns a new socket binded to the Referee."""
        sock = socket.socket(
            socket.AF_INET, 
            socket.SOCK_DGRAM, 
            socket.IPPROTO_UDP
        )

        sock.setsockopt(
            socket.SOL_SOCKET, 
            socket.SO_REUSEADDR, 1
        )

        sock.bind((self.host, self.referee_port))

        mreq = struct.pack(
            "4sl",
            socket.inet_aton(self.host),
            socket.INADDR_ANY
        )

        sock.setsockopt(
            socket.IPPROTO_IP, 
            socket.IP_ADD_MEMBERSHIP, 
            mreq
        )

        return sock

if __name__ == "__main__":
    r = RefereeComm()
    r.start()
