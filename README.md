# pico-drama
Pi Pico pwm controller

This was used to control a number of lamps via PWM pins on a Pi PICO.

(see Scenes.py) 
The 'lamps'  are initially named with pin numbers in a dictionary string which will create 'lamp' objects when added to the 
'production' object.
'scenarios' (containing list of named lamps and fade value and delay value) are collected into 'acts' with repeat counters
when added to the 'production' class object these create 'act' and 'scene' objects :
