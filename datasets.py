import csv
dhi = []
dni = []
dbt = []
wind = []
with open("usa.csv","r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        dhi.append(float(row["Diffuse Horizontal Radiation {Wh/m2}"]))
        dni.append(float(row["Direct Normal Radiation {Wh/m2}"]))
        dbt.append(float(row["Dry Bulb Temperature {C}"]))
        wind.append(float(row["Wind Speed {m/s}"]))
        



print(dhi[2])    
print(dni[10]) 
print(dbt[10]) 
print(wind[10])  



