#Written By: Nathan Aruna and Christos Velmachos

#<----safe/normal conditions---->
sampleData = {
  "lpg": 1.2,
  "ch4": 1.9,     
  "h2": 0.5,       
  "CO": 0.1,
  "C": 20,
}

#<----notsafe/notnormal conditions---->
sampleData2 = {
  "lpg": 1000,     #in ppm
  "ch4": 700,      #in ppm
  "h2": 1000,       #in ppm
  "CO": 150,       #in ppm
  "C": 39.5,       #in celcius
}

lpg = float(input("What is the ppm of lpg?")) - 1 #normal ppm is 1
ch4 = float(input("What is the ppm of ch4?")) - 1.86 #normal ppm is 1.86
h2 = float(input("What is the ppm of h2?")) - 0.5 #normal ppm is 700
co = float(input("What is the ppm of co?")) - 0.1 #normal ppm is 0.1
c = float(input("What is the temperature?")) - 20  #normal celcius is 20

N1 = float(lpg / 990)
N2 = float(ch4 / 950)
N3 = float(co / 199.5)
N4 = float(c / 44)
N5 = float(h2 / 1999.5)

#to not cause any conflicts between etlu and standarized etlu
StandarizedEtlu = (0.30 * N1) + (0.20 * N2) + (0.25 * N3) + (0.10 * N4)+ (0.15 * N5)

#will always return a positive value
etlu = abs(StandarizedEtlu * 100 / 2)


for sample in sampleData:
  print(sample, sampleData[sample])

print("ETLU:", etlu) #closer value is to 0, the safer it is
                     #closer value is to 50, the more dangerous it is