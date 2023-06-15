from XInput import *

index = 0

while(1):
    vals = get_thumb_values(get_state(0))
    print(vals[0], vals[1])
