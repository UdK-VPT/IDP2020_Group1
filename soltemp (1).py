import csv

GTI1= []
GTI2= []
GTI3= []
GTI4= []
GTI5= []
wind =[]
dbt=[]
Tsol1=[]
Tsol2=[]
Tsol3=[]
Tsol4=[]
Tsol5=[]
Tw1=[]
Tw2=[]
Tw3=[]
Tw4=[]
Tw5=[]
t1=[]   # thickness
t2=[]
t3=[]
t4=[]
t5=[]
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
I_wall=0          # W/m2
Fm1=(A1/(A1+A2+A3+A4+A5+A6))      # view factor for person to outside
Fm2=(A2/(A1+A2+A3+A4+A5+A6))
Fm3=(A3/(A1+A2+A3+A4+A5+A6))
Fm4=(A4/(A1+A2+A3+A4+A5+A6))
Fm5=(A5/(A1+A2+A3+A4+A5+A6))
Theat=[]
Tcool=[]
thkheat=[]
thkcool=[]
Troom=[]
p=0
deltaheat=0
Heating_hours=0
deltacool=0
Cooling_hours=0


with open("USA_CO_Golden-NREL.724666_TMY3EPW.csv","r") as file:    #location will change
    reader = csv.DictReader(file)

    for row in reader:
        dbt.append(float(row["Dry Bulb Temperature {C}"]))
        

tstart=dbt[0]

for x in range(0,8760):
  if construction=="concrete":
      Tsol1[x]=dbt[x] + R_wall * (absorptivity_concrete*GTI[x])
      Tsol2[x]=dbt[x] + R_wall * (absorptivity_concrete*GTI[x])
      Tsol3[x]=dbt[x] + R_wall * (absorptivity_concrete*GTI[x])
      Tsol4[x]=dbt[x] + R_wall * (absorptivity_concrete*GTI[x])
      Tsol5[x]=dbt[x] + R_roof * ((absorptivity_concrete*GTI[x])-(emmisivity_concrete*I_roof))
  if construction=="brick":
      Tsol1[x]=dbt[x] + R_wall * (absorptivity_brick*GTI[x])
      Tsol2[x]=dbt[x] + R_wall * (absorptivity_brick*GTI[x])
      Tsol3[x]=dbt[x] + R_wall * (absorptivity_brick*GTI[x])
      Tsol4[x]=dbt[x] + R_wall * (absorptivity_brick*GTI[x])
      Tsol5[x]=dbt[x] + R_roof * ((absorptivity_brick*GTI[x])-(emmisivity_brick*I_roof))


    
for y in range(0,8760):
    if (GTI1[y]+ GTI2[y] + GTI3[y] + GTI4[y] + GTI5[y]) == 0:
        for z in range(20,46,1):
            i=0
            j=0
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
                p=1
                break
            elif Treq[z-20]< min_temp:
                Theat[i]= min_temp-Treq[z-20]
                thkheat[i]=z
                i=i+1
            elif Treq[z-20]> max_temp:
                Tcool[j]=Treq[z-20]-max_temp
                thkcool[j]=z
                j=j+1


        if(p==1):
            p=0
            break
        elif(i>0):
            pos = Theat.index(min(Theat))
            t1[y]= thkheat[pos]            # thickness
            t2[y]= thkheat[pos] 
            t3[y]= thkheat[pos] 
            t4[y]= thkheat[pos] 
            t5[y]= thkheat[pos] 
        elif(j>0):
            pos1 = Theat.index(min(Tcool))
            t1[y]= thkcool[pos1]            # thickness
            t2[y]= thkcool[pos1] 
            t3[y]= thkcool[pos1] 
            t4[y]= thkcool[pos1] 
            t5[y]= thkcool[pos1] 


    if (GTI1[y]+ GTI2[y] + GTI3[y] + GTI4[y] + GTI5[y])!=0:
        for z in range(20,46,1):
            i=0
            j=0
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
                break
            elif Treq[z-20]< min_temp:
                Theat[i]= min_temp-Treq[z-20]
                thkheat[i]=z
                i=i+1
            elif Treq[z-20]> max_temp:
                Tcool[j]=Treq[z-20]-max_temp
                thkcool[j]=z
                j=j+1


        if(p==1):
            p=0
            break
        elif(i>0):
            pos = Theat.index(min(Theat))
            t1[y]= thkheat[pos]            # thickness
            t2[y]= thkheat[pos] 
            t3[y]= thkheat[pos] 
            t4[y]= thkheat[pos] 
            t5[y]= thkheat[pos] 

        elif(j>0):
            pos1 = Theat.index(min(Tcool))
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


for q in range(0,8760):
    if Troom[q]>=min_temp and Troom[q]<=max_temp:
        comfort = comfort+1
    elif Troom[q]<min_temp:
        Heat_hours= Heat_hours+1
        deltaheat= min_temp-Troom[q]
        hour_heat[a]=q
        Qheat[a] = (1.225*(Volume_of_room)*1000*deltaheat)/3600
        a=a+1
    elif Troom[q]>man_temp:
        Cool_hours= Cool_hours+1
        deltacool= Troom[q]-min_temp
        hour_cool[b]=q
        Qcool[b] = (1.225*(Volume_of_room)*1000*deltacool)/3600
        b=b+1




   
# creating the dataset 
fig = plt.figure(figsize = (10, 5)) 
  
# creating the bar plot 
plt.bar(Troom, color ='maroon') 
  
plt.xlabel("No. of hours") 
plt.ylabel("Room Temperature") 
plt.title("Variation of room temperature with suggested mean thickness") 
plt.show()
        
        






