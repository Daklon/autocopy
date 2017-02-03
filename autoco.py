from subprocess import call
import os
import glob
import settings
import time

disks = []
temp_disk = []

def ddcopy():
    call(['dd','if='+file,'of='+settings.DD_SAVE_DIR+time.strftime('%S:%H-%d-%m-%Y]',time.gmtime())+'.iso'])

while True:
    os.chdir('/dev/disk/by-path') #directorio donde buscar los discos y particiones
    for file in glob.glob('*[usb]*'): #filtro para solo mostrar los dispositivos usb
        temp_disk.append(file)
        if disks.count(file) == 0:
            disks.append(file) #guardo en una lista cada uno de los archivos
            if 'part' in file:
                print('PART:\n'+file)
            else:
                print('DISK:\n'+file)
             
         
            
