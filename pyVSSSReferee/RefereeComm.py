import abc
import os
import json
import struct
import socket
import threading
import time

from google.protobuf.json_format import MessageToJson
from .protocols import vssref_command_pb2, vssref_placement_pb2, vssref_common_pb2

def get_config(config_file=None):
    """Return parsed config_file."""
    if config_file:
        config = json.loads(open(config_file, 'r').read())
    else:
        config = json.loads(open('config.json', 'r').read())

    return config

class RefereeComm(threading.Thread):
    
    def __init__(self, config_file = None):
        """The RefereeComm class creates a socket to communicate with the Referee.

        Methods:
            run(): calls _create_socket() and parses the status message from the Referee.
            can_play(): returns true if game is currently on GAME_ON.
            get_last_foul(): Returns last foul information.
            get_status(): returns current status message sent by the referee.
            get_color(): Returns color of the team that will kick in the penalty or goal kick.
            get_quadrant(): Returns the quandrant in which the free ball will occur.
            get_foul(): Return current foul.
            _create_socket(): returns new socket binded to the Referee.
        """
        super(RefereeComm, self).__init__()
        self.config = get_config(config_file)
        self.commands = []

        self._status = None

        self.referee_port = int(os.environ.get('REFEREE_PORT', self.config['network']['referee_port']))
        self.host = os.environ.get('REFEREE_IP', self.config['network']['referee_ip'])
        self.replacer_port = int(os.environ.get('REPLACER_PORT', self.config['network']['replacer_port']))

        self.referee_sock = None

        self._can_play = False
        self._color = None
        self._quadrant = None
        self._foul = None
    
    def get_last_foul(self):
        """Returns last foul information.

        Returns foul, quadrant, color and can_play (true if foul is GAME_ON).
        """
        
        return {
            'foul': self._foul,
            'quadrant': self._quadrant,
            'color': self._color,
            'can_play': self._can_play
        }
    
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

            self._can_play = self._status.get('foul') == 'GAME_ON'
            if (self._status.get('foul') != 'GAME_ON'):
                self._foul = self._status.get('foul')
            if (self._status.get('foul') == 'FREE_BALL'):
                self._quadrant = self._status.get('foulQuadrant')
            elif (self._status.get('foul') == 'PENALTY_KICK' or self._status.get('foul') == 'GOAL_KICK'):
                self._color = self._status.get('teamcolor', 'BLUE')

    def can_play(self):
        """Returns if game is currently on GAME_ON."""
        return self._can_play

    def get_status(self):
        """Returns current status message sent by the referee."""
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

    def send_replacement(self, robot_replacements, team_color):
        """Receives team color and list of x and y coordinates, angle and ids of robots and sends to Referee.
        
        Team color must be in uppercase, either 'BLUE' or 'YELLOW'.
        """

        replacements = vssref_placement_pb2.VSSRef_Placement()
        frame = vssref_common_pb2.Frame()
        frame.teamColor = 0 if team_color == "BLUE" else 1
        for robot in robot_replacements:
            replacement = frame.robots.add()
            replacement.robot_id = robot['robot_id']
            replacement.x = robot['x']
            replacement.y = robot['y']
            replacement.orientation = robot['orientation']
        replacements.world.CopyFrom(frame)
        self.referee_sock.sendto(replacements.SerializeToString(), (self.host, self.replacer_port))
        

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
