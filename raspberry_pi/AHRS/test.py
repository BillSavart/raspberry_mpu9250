import numpy as np
import math

roll = 1
pitch = -85
yaw = -85

qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

print(qx)
print(qy)
print(qz)
print(qw)
print

roll = math.degrees((math.atan2(qx*qy + qz*qw, 0.5 - qy*qy - qz*qz)))
pitch = math.degrees((math.asin(-2.0 * (qy*qw - qx*qz))))
yaw = math.degrees((math.atan2(qy*qz + qx*qw, 0.5 - qz*qz - qw*qw)))

print(roll)
print(pitch)
print(yaw)
print
