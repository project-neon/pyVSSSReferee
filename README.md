# pyVSSSReferee
Easily create a network socket between the VSSS League's referee and your VSSS software.


## Requirements
- protobuf==3.6.1

## Installation
Use the code below to install the package from PyPI:

`pip install pyVSSSReferee`

## A Simple Example
1. In a test folder, save the code below as config.json

```
{
    "network" : {
        "multicast_ip": "224.0.0.1",
        "referee_ip": "224.5.23.2",
        "host_ip": "localhost",
        "blue_port": 30011,
        "yellow_port": 30012,
        "vision_port": 10002,
        "command_port": 20011,
        "referee_port": 10003,
        "replacer_port": 10004
    },
    "match" : {
        "num_robots": 3,
        "team_color": "blue"
    }
}
```

2. In the same folder, save the code below as test.py and run it while the referee is running

```
import pyVSSSReferee

from pyVSSSReferee.RefereeComm import RefereeComm

r = RefereeComm(config_file = "config.json")
r.start()
while (True):
    print(r.get_last_foul())

```

## Important Methods
Some important methods are:
| Method | Description |
| ------ | ------ |
| get_last_foul | Returns last foul in the format: {'foul': 'Foul_name', 'quadrant': 'Quadrant_number', 'color': 'Team_color', 'can_play': 'boolean_value'} |
| can_play | Returns True if current game foul is GAME_ON, returns False otherwise |
| get_status | Returns game's current status message sent by the referee |
| get_color | Returns color of the team that will kick in the penalty or goal kick. BLUE is default. |
| get_quadrant | Returns the quandrant in which the free ball will occur. |
| get_foul | Returns current foul. |
| send_replacement | Receives team color and list of x and y coordinates, angle and ids of robots and sends to the Referee. Team color must be in uppercase, either 'BLUE' or 'YELLOW'. |

## Colaboration Guide
In order to colaborate with this repository, clone this repository:

`git clone https://github.com/project-neon/pyVSSSReferee`

Open directory

`cd pyVSSSReferee`

Then install dependencies

`pip install -r requirements.txt`

Finally, install the package

`python3 setup.py install`


Remember to use the Project Neon guidelines to git:
https://github.com/project-neon/codestyleguide/blob/master/git.md
