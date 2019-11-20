## Design Doc
[Project design doc](https://docs.google.com/document/d/1Ugk2y4TebeorE_mTjUtP9OOJdkafuY8iWdb1rNmWi6s/edit?fbclid=IwAR1iq-N0wK0B4ZswSTv36Xpg0mgAYl4u9vF7Ml6ew7K8e-IRKzPsV26zWQI#)

## Setup Instructions
- [Install Python 3](https://www.python.org/downloads/)
- [Clone the tetris game repo](https://github.com/LoveDaisy/tetris_game)
- Install pyQt5 and numpy, required to run the game
  - py -3.8 -m pip install pyQt5
  - py -3.8 -m pip install numpy

## Injection script running instructions
```
usage: inject.py [-h] repo logger
  positional arguments:
  repo        path of the repo to be analyzed
  logger      full path of logger script
```

Example run
```
py -3.8 inject.py "D:\CPSC 410 Software engineering\Visualization_repo\tetris_game" "D:\CPSC 410 Software engineering\Visualization_repo\src\loggerAPI.py"
```
