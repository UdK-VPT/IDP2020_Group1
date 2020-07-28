import math

lat = 23.23
lng = 56.56
ts = 2.5
vs = []
az = []
  
for day in range(365):
    J=360*(day)/365
    delta=(0.3948-23.2559*math.cos(math.radians(J+9.1))-0.3915*math.cos(math.radians(2*J+5.4))-0.1764*math.cos(math.radians(3*J+26)))
    teq=( 0.0066+7.3525*math.cos(math.radians(J+85.9)) + 9.9359*math.cos(math.radians(2*J+108.9)) + 0.3387*math.cos(math.radians(3*J+105.2)) )/60
    for UTC in range(24):
        LMT = UTC-4*(15*ts-lng)/60
        LT = LMT + teq
        omega=(12-LT)*15
        vsdummy=math.degrees(math.asin(math.sin(math.radians(lat))*math.sin(math.radians(delta))+math.cos(math.radians(lat))*math.cos(math.radians(delta))*math.cos(math.radians(omega))))
        vs.append(vsdummy)
        if LT <= 12:
            azdummy=180-math.degrees(math.acos((math.sin(math.radians(vs[(day)*24+UTC]))*math.sin(math.radians(lat))-math.sin(math.radians(delta)))/(math.cos(math.radians(vs[(day)*24+UTC]))*math.cos(math.radians(lat)))))
            az.append(azdummy)
        else:
            azdummy=180+math.degrees(math.acos((math.sin(math.radians(vs[(day)*24+UTC]))*math.sin(math.radians(lat))-math.sin(math.radians(delta)))/(math.cos(math.radians(vs[(day)*24+UTC]))*math.cos(math.radians(lat)))))
            az.append(azdummy)

    tg = []
    ve1 = 0
    ve2 = 90
    ae1 = 0
    ae2 = ae1+90
    if ae2 > 360:
        ae2 = ae2 - 360
    ae3 = ae2 + 90
    if ae3 > 360:
        ae3 = ae3 - 360
    ae4 = ae3 + 90
    if ae4 > 360:
        ae4 = ae4 - 360    
    ae5 = 0
    for i in range(8760):
        theta = math.degrees(math.acos(-math.cos(math.radians(vs[i]))*math.sin(math.radians(ve2))*math.cos(math.radians((az[i]-ae1))+math.sin(math.radians(vs[i]))*math.cos(math.radians(ve2)))))