import math
Kp = 2.0 
Ki = 0.005 
halfT = 0.5 

q0 = 1
q1 = 0
q2 = 0
q3 = 0
exInt = 0
eyInt = 0
ezInt = 0
gx = 0
gy = 0
gz = 0
ax = 0
ay = 0
az = 0
mx = 0
my = 0
mz = 0
norm = 0
hx = 0
hy = 0
hz = 0
bx = 0
bz = 0
vx = 0
vy = 0
vz = 0
wx = 0
wy = 0
wz = 0
ex = 0
ey = 0
ez = 0

q0q0 = q0*q0
q0q1 = q0*q1
q0q2 = q0*q2
q0q3 = q0*q3
q1q1 = q1*q1
q1q2 = q1*q2
q1q3 = q1*q3
q2q2 = q2*q2
q2q3 = q2*q3
q3q3 = q3*q3     

norm = math.sqrt(ax*ax + ay*ay + az*az)  
ax = ax / norm
ay = ay / norm
az = az / norm
norm = math.sqrt(mx*mx + my*my + mz*mz)    
mx = mx / norm
my = my / norm
mz = mz / norm        

hx = 2.0*mx*(0.5 - q2q2 - q3q3) + 2.0*my*(q1q2 - q0q3) + 2.0*mz*(q1q3 + q0q2)
hy = 2.0*mx*(q1q2 + q0q3) + 2.0*my*(0.5 - q1q1 - q3q3) + 2.0*mz*(q2q3 - q0q1)
hz = 2.0*mx*(q1q3 - q0q2) + 2.0*my*(q2q3 + q0q1) + 2.0*mz*(0.5 - q1q1 - q2q2)   
bx = math.sqrt((hx*hx) + (hy*hy))
bz = hz

vx = 2.0*(q1q3 - q0q2)
vy = 2.0*(q0q1 + q2q3)
vz = q0q0 - q1q1 - q2q2 + q3q3
wx = 2.0*bx*(0.5 - q2q2 - q3q3) + 2.0*bz*(q1q3 - q0q2)
wy = 2.0*bx*(q1q2 - q0q3) + 2.0*bz*(q0q1 + q2q3)
wz = 2.0*bx*(q0q2 + q1q3) + 2.0*bz*(0.5 - q1q1 - q2q2)

ex = (ay*vz - az*vy) + (my*wz - mz*wy)
ey = (az*vx - ax*vz) + (mz*wx - mx*wz)
ez = (ax*vy - ay*vx) + (mx*wy - my*wx)

exInt = exInt + ex*Ki
eyInt = eyInt + ey*Ki
ezInt = ezInt + ez*Ki

gx = gx + Kp*ex + exInt
gy = gy + Kp*ey + eyInt
gz = gz + Kp*ez + ezInt

q0 = q0 + (-q1*gx - q2*gy - q3*gz)*halfT
q1 = q1 + (q0*gx + q2*gz - q3*gy)*halfT
q2 = q2 + (q0*gy - q1*gz + q3*gx)*halfT
q3 = q3 + (q0*gz + q1*gy - q2*gx)*halfT;  

norm = math.sqrt(q0*q0 + q1*q1 + q2*q2 + q3*q3)
q0 = q0 / norm
q1 = q1 / norm
q2 = q2 / norm
q3 = q3 / norm