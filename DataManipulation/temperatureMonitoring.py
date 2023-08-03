import os 
import time


sampleTemps = {
    'TempSens1': 70, #internal temp
    'TempSens2': 35, #water probe
    'TempSens3': 40, #air temp
}

def userWarning():
   print('WARNING: Internal temperature is too high')
   print(str(sampleTemps['TempSens1']) + '°C')

def warningOverideMode():
   sampleTemps['TempSens1'] = 0
   print('Mode: Warming Overide')
   

def sysShutdownWarning():
    print('WARNING: System will shutdown Shortly Due to High Internal Temperature')
    print(str(sampleTemps['TempSens1']) + '°C')

def sysShutdown():
   os.system('sudo shutdown -h now')


while True:
   print('Internal Temperature: ' + str(sampleTemps['TempSens1']) + '°C')

   if sampleTemps['TempSens1'] > 60:
     print('Internal Temperature is too high')
     time.sleep(10)

   if sampleTemps['TempSens1'] > 60:
        
        overide = str(input('Would you like to overide temperature warning? y/n:'))

        if overide == 'y':
           warningOverideMode()
           break
         
        else:
           sysShutdownWarning()
           time.sleep(5) 
           sysShutdown()
             
        
      
      



