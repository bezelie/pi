# Bezelie Sample Code for Raspberry Pi : Servo Centering

from  time import sleep
import bezelie

# Pitch
bezelie.movePit (45)
sleep (0.5)
bezelie.movePit (-45)
sleep (0.5)
bezelie.movePit (0)
sleep (0.5)

# Rotation
bezelie.moveRot (45)
sleep (0.5)
bezelie.moveRot (-45)
sleep (0.5)
bezelie.moveRot (0)
sleep (0.5)

# Yaw
bezelie.moveYaw (45)
sleep (0.5)
bezelie.moveYaw (-45)
sleep (0.5)
bezelie.moveYaw (0)
sleep (0.5)
