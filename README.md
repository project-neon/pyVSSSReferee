# pyVSSSReferee
Easily create a network socket between the VSSS League's referee and your VSSS software.


## Requirements
- protobuf==3.6.1

## Installation
1. Clone this repository
`git clone https://github.com/project-neon/pyVSSSReferee`

2. Open directory
`cd pyVSSSReferee`

3. Install dependencies
`pip install -r requirements.txt`


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

## A Simple Example
```
# You can save this as test.py and run it
import pyVSSSReferee

from pyVSSSReferee.RefereeComm import RefereeComm

r = RefereeComm(config_file = "blue_team.json")
r.start()
while (True):
    print(r.get_last_foul())

```
