from flask import Flask, render_template, request
import math
import csv


latitude = "NaN"
longitude = "NaN"
time_shift = "NaN"
vs = []
az = []
construction = "concrete"
GTI1 = []
GTI2 = []
GTI3 = []
GTI4 = []
GTI5 = []
dbt = []



app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index.html')
def indexone():
    return render_template("index.html")

@app.route('/locations.html')
def locations():
    return render_template("locations.html")

@app.route('/buildings.html')
def buildings():
    return render_template("buildings.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")        

@app.route('/creators.html')
def creators():
    return render_template("creators.html")

@app.route('/data.html')
def data():
    return render_template("data.html")

@app.route('/rooms.html')
def rooms():
    return render_template("rooms.html")  

@app.route('/user_location.html')
def user_location():
    return render_template("user_location.html")      

@app.route('/input1')
def input1():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    time_shift = request.args.get("time_shift")
    lat = float(latitude)
    lng = float(longitude)
    ts = float(time_shift)
    
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
    return render_template("compass.html")

@app.route('/compass') 
def compass():
    dhi = []
    dni = []

    tg1 = []
    tg2 = []
    tg3 = []
    tg4 = []
    tg5 = []
    ve1 = 0
    ve2 = 90
    azimuth = request.args.get("azimuth")
    ae1 = float(azimuth)
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
        theta1 = math.degrees(math.acos(-math.cos(math.radians(vs[i]))*math.sin(math.radians(ve2))*math.cos(math.radians((az[i]-ae1))+math.sin(math.radians(vs[i]))*math.cos(math.radians(ve2)))))
        theta2 = math.degrees(math.acos(-math.cos(math.radians(vs[i]))*math.sin(math.radians(ve2))*math.cos(math.radians((az[i]-ae2))+math.sin(math.radians(vs[i]))*math.cos(math.radians(ve2)))))
        theta3 = math.degrees(math.acos(-math.cos(math.radians(vs[i]))*math.sin(math.radians(ve2))*math.cos(math.radians((az[i]-ae3))+math.sin(math.radians(vs[i]))*math.cos(math.radians(ve2)))))
        theta4 = math.degrees(math.acos(-math.cos(math.radians(vs[i]))*math.sin(math.radians(ve2))*math.cos(math.radians((az[i]-ae4))+math.sin(math.radians(vs[i]))*math.cos(math.radians(ve2)))))
        theta5 = math.degrees(math.acos(-math.cos(math.radians(vs[i]))*math.sin(math.radians(ve1))*math.cos(math.radians((az[i]-ae5))+math.sin(math.radians(vs[i]))*math.cos(math.radians(ve1)))))
        tg1.append(theta1)
        tg2.append(theta2)
        tg3.append(theta3)
        tg4.append(theta4)
        tg5.append(theta5)
    #HERE YOU NEED THE CORRECT CSV FILE LOADED
    #THINK OF A LOGIC
    with open("usa.csv","r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dhi.append(float(row["Diffuse Horizontal Radiation {Wh/m2}"]))
            dni.append(float(row["Direct Normal Radiation {Wh/m2}"]))
            dbt.append(float(row["Dry Bulb Temperature {C}"]))   
    for j in range(8760):
        irr1 = (dni[j]* math.sin(math.radians(vs[j]))) * math.cos(math.radians(tg1[j])) / math.sin(math.radians(vs[j]))  + dhi[j] * 0.5 * (1+math.cos(math.radians(ve2)))
        irr2 = (dni[j]* math.sin(math.radians(vs[j]))) * math.cos(math.radians(tg2[j])) / math.sin(math.radians(vs[j]))  + dhi[j] * 0.5 * (1+math.cos(math.radians(ve2)))
        irr3 = (dni[j]* math.sin(math.radians(vs[j]))) * math.cos(math.radians(tg3[j])) / math.sin(math.radians(vs[j]))  + dhi[j] * 0.5 * (1+math.cos(math.radians(ve2)))
        irr4 = (dni[j]* math.sin(math.radians(vs[j]))) * math.cos(math.radians(tg4[j])) / math.sin(math.radians(vs[j]))  + dhi[j] * 0.5 * (1+math.cos(math.radians(ve2)))
        irr5 = (dni[j]* math.sin(math.radians(vs[j]))) * math.cos(math.radians(tg5[j])) / math.sin(math.radians(vs[j]))  + dhi[j] * 0.5 * (1+math.cos(math.radians(ve1)))
        GTI1.append(irr1)
        GTI2.append(irr2)         
        GTI3.append(irr3)         
        GTI4.append(irr4)         
        GTI5.append(irr5)         

    return render_template("building_details.html")
 
@app.route('/input2')
def input2(): 
    length = float(request.args.get("length"))
    breadth = float(request.args.get("breadth"))   
    height = float(request.args.get("height"))

Tsol1=[0]*8760  
Tsol2=[0]*8760
Tsol3=[0]*8760
Tsol4=[0]*8760
Tsol5=[0]*8760
Tw1=[0]*8760
Tw2=[0]*8760
Tw3=[0]*8760
Tw4=[0]*8760
Tw5=[0]*8760
t1=[0]*8760   # thickness
t2=[0]*8760
t3=[0]*8760
t4=[0]*8760
t5=[0]*8760
A1=length*height
A2=breadth*height
A3=length*height
A4=breadth*height
A5=length*breadth
A6=length*breadth
Volume_of_room = length*breadth*height
emmisivity_brick = 0.55
absorptivity_brick = 0.93
emmisivity_concrete = 0.65
absorptivity_concrete = 0.96
max_temp = 18
min_temp = 24
R_wall=0.05       # m2K/W
R_roof=0.04       # m2K/W
I_roof=100        # W/m2
#I_wall=0          # W/m2
Fm1=(A1/(A1+A2+A3+A4+A5+A6))      # view factor for person to outside
Fm2=(A2/(A1+A2+A3+A4+A5+A6))
Fm3=(A3/(A1+A2+A3+A4+A5+A6))
Fm4=(A4/(A1+A2+A3+A4+A5+A6))
Fm5=(A5/(A1+A2+A3+A4+A5+A6))
Theat=[]
Tcool=[]
Qheat = []
Qcool = []
hour_heat = []
hour_cool = []
thkheat=[]
thkcool=[]
Troom=[] #*8760
Treq = []
p=0
o=0
deltaheat=0
Heat_hours=0
deltacool=0
Cool_hours=0
for x in range(0,8760):
    if construction=="concrete":
        Tsol1[x]=dbt[x] + R_wall * (absorptivity_concrete*GTI1[x])
        Tsol2[x]=dbt[x] + R_wall * (absorptivity_concrete*GTI2[x])
        Tsol3[x]=dbt[x] + R_wall * (absorptivity_concrete*GTI3[x])
        Tsol4[x]=dbt[x] + R_wall * (absorptivity_concrete*GTI4[x])
        Tsol5[x]=dbt[x] + R_roof * ((absorptivity_concrete*GTI5[x])-(emmisivity_concrete*I_roof))
    if construction=="brick":
        Tsol1[x]=dbt[x] + R_wall * (absorptivity_brick*GTI1[x])
        Tsol2[x]=dbt[x] + R_wall * (absorptivity_brick*GTI2[x])
        Tsol3[x]=dbt[x] + R_wall * (absorptivity_brick*GTI3[x])
        Tsol4[x]=dbt[x] + R_wall * (absorptivity_brick*GTI4[x])
        Tsol5[x]=dbt[x] + R_roof * ((absorptivity_brick*GTI5[x])-(emmisivity_brick*I_roof))

for y in range(0,8760):
    if (GTI1[y]+ GTI2[y] + GTI3[y] + GTI4[y] + GTI5[y]) == 0:
        m=0
        n=0
        for z in range(20,46,1):
            Tw1[y]=Tsol1[y] - ((4*z)/100)
            Tw2[y]=Tsol2[y] - ((4*z)/100)
            Tw3[y]=Tsol3[y] - ((4*z)/100)
            Tw4[y]=Tsol4[y] - ((4*z)/100)
            Tw5[y]=Tsol5[y] - ((4*z)/100)
            Treq[z-20] = Fm1*Tw1[y] + Fm2*Tw2[y] + Fm3*Tw3[y] + Fm4*Tw4[y] + Fm5*Tw5[y]
            if Treq[z-20]>=min_temp and Treq[z-20]<=max_temp:
                t1[y]= z   # thickness
                t2[y]= z
                t3[y]= z
                t4[y]= z
                t5[y]= z
                o=1
                
            elif Treq[z-20]< min_temp:
                th= min_temp-Treq[z-20]
                Theat.append(th)
                thkh=z
                thkheat.append(thkh)
                m=m+1
            elif Treq[z-20]> max_temp:
                tc=Treq[z-20]-max_temp
                Tcool.append(tc)
                thkc=z
                thkcool.append(thkc)
                n=n+1


        if(o==1):# define it
            o=0
            
        elif(m>0):
            mini2 = min(Theat) # change
            pos2 = Theat.index(mini2)
            t1[y]= thkheat[pos]            # thickness
            t2[y]= thkheat[pos] 
            t3[y]= thkheat[pos] 
            t4[y]= thkheat[pos] 
            t5[y]= thkheat[pos] 
        elif(n>0):
            mini3 = min(Tcool)
            pos3 = Tcool.index(mini3) # add new variable mini
            t1[y]= thkcool[pos1]            # thickness
            t2[y]= thkcool[pos1] 
            t3[y]= thkcool[pos1] 
            t4[y]= thkcool[pos1] 
            t5[y]= thkcool[pos1] 


    if (GTI1[y]+ GTI2[y] + GTI3[y] + GTI4[y] + GTI5[y])!=0:
        i=0
        j=0            
        for z in range(20,46,1):
            Tw1[y]=Tsol1[y] + ((4*z)/100)
            Tw2[y]=Tsol2[y] + ((4*z)/100)
            Tw3[y]=Tsol3[y] + ((4*z)/100)
            Tw4[y]=Tsol4[y] + ((4*z)/100)
            Tw5[y]=Tsol5[y] + ((4*z)/100)
            Treq[z-20] = Fm1*Tw1[y] + Fm2*Tw2[y] + Fm3*Tw3[y] + Fm4*Tw4[y] + Fm5*Tw5[y]
            if Treq[z-20]>=min_temp and Treq[z-20]<=max_temp:
                t1[y]= z   # thickness
                t2[y]= z
                t3[y]= z
                t4[y]= z
                t5[y]= z
                p=1
                
            elif Treq[z-20]< min_temp: 
                th= min_temp-Treq[z-20] #change
                Theat.append(th)
                thkh=z
                thkheat.append(thkh)
                i=i+1
            elif Treq[z-20]> max_temp: #change
                tc=Treq[z-20]-max_temp
                Tcool.append(tc)
                thkc=z
                thkcool.append(thkc)
                j=j+1


        if(p==1):
            p=0
        
        elif(i>0):
            mini = min(Theat)
            pos = Theat.index(mini)
            t1[y]= thkheat[pos]            # thickness
            t2[y]= thkheat[pos] 
            t3[y]= thkheat[pos] 
            t4[y]= thkheat[pos] 
            t5[y]= thkheat[pos] 

        elif(j>0):
            mini1 = min(Tcool)
            pos1 = Tcool.index(mini1) # add new variable mini3 and pos3
            t1[y]= thkcool[pos1]            # thickness
            t2[y]= thkcool[pos1] 
            t3[y]= thkcool[pos1] 
            t4[y]= thkcool[pos1] 
            t5[y]= thkcool[pos1] 


Thickness1 = sum(t1)/8760
Thickness2 = sum(t2)/8760
Thickness3 = sum(t3)/8760
Thickness4 = sum(t4)/8760
Thickness5 = sum(t5)/8760

for s in range(0,8760):
    Tw1[s]=Tsol1[s] + Thickness1/100
    Tw2[s]=Tsol2[s] + Thickness2/100
    Tw3[s]=Tsol3[s] + Thickness3/100
    Tw4[s]=Tsol4[s] + Thickness4/100
    Tw5[s]=Tsol5[s] + Thickness5/100
    Troom[s]= Fm1*Tw1[s] + Fm2*Tw2[s] + Fm3*Tw3[s] + Fm4*Tw4[s] + Fm5*Tw5[s]

a=b=0
for q in range(0,8760):
    if Troom[q]>=min_temp and Troom[q]<=max_temp:
        comfort = comfort+1
    elif Troom[q]<min_temp:
        Heat_hours= Heat_hours+1
        deltaheat= min_temp-Troom[q]
        hour_heat[a]=q
        Qh= (1.225*(Volume_of_room)*1000*deltaheat)/3600
        Qheat.append(Qh)
        
        a=a+1
    elif Troom[q]>max_temp:
        Cool_hours= Cool_hours+1
        deltacool= Troom[q]-min_temp
        hour_cool[b]=q
        Qc = (1.225*(Volume_of_room)*1000*deltacool)/3600
        Qcool.append(Qc)
        b=b+1

        

    
