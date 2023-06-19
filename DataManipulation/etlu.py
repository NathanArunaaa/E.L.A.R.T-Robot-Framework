#Written By: Nathan Aruna

#<----safe/normal conditions---->
sampleData = {
  "msv": 1.2,
  "CO2": 700,
  "CO": 0.1,
  "C": 20,
}

#<----notsafe/notnormal conditions---->
sampleData2 = {
  "msv": 500,      #in msv
  "CO2": 40000,    #in ppm
  "CO": 150,       #in ppm
  "C": 39.5,       #in celcius
}

msv = sampleData["msv"] - 1.8 #normal msv is 1.8
co2 = sampleData["CO2"] - 700 #normal ppm is 700
co = sampleData["CO"] - 0.1 #normal ppm is 0.1
c = sampleData["C"] - 20  #normal celcius is 20

N1 = float(msv / 99998.2)
N2 = float(co2 / 39600)
N3 = float(co / 199.5)
N4 = float(c / 44)

etlu = (0.35 * N1) + (0.25 * N2) + (0.25 * N3) + (0.15 * N4)

#will always return a positive value
etlu = abs(etlu * 100)


for sample in sampleData:
  print(sample, sampleData[sample])

print("ETLU:", etlu) #closer value is to 0, the safer it is
                     #closer value is to 50, the more dangerous it is