Get started

1) Install Python (python3 recommended, or python2) and pip

2) Install lifxlan from mclarkk 
    (one of the following)
    sudo pip install lifxlan
    sudo pip3 install lifxlan
    sudo python3 -m pip install lifxlan

3) Install pynput
    (one of the following)
    sudo pip install pynput
    sudo pip3 install pynput
    sudo python3 -m pip install pynput

4) These may be other packages required such as bitstring and netifaces. Install using the same methods as above.

5) Make sure your lifx z light strip is turned on and on the same network

6) Run the python script. It will automatically discover your light and then start the code (if it failes to find your light try running it again)

Controls:
    # If space key is pressed change the snake colour
    # If down right shift key is pressed change the background colour
    # If up key is pressed increase the snake size by 1
    # If down key is pressed decrease the snake size by 1
    # If left arrow key is pressed move the snake left 1
    # If right arrow key is pressed move the snake right 1