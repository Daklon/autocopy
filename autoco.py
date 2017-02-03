from subprocess import call
import os
import glob
import settings
import time
import re

disks = []
temp_disk = []

def check_action(file):
    ##AQUÍ FALTA MUCHO CÓDIGO##
    actions = {'1':ddcopy,'2':filecopy}
    results = [s for s in re.split(':',file)] #parte la cadena en campos, usa ":" como separador para obtener el puerto del pendrive
    puerto = results.pop(3)

#Realiza la copia de ficheros(usa la partición, no el disco), es mas rápida que el dd pero a costa de copiar menos información
#Guarda en FC_SAVE_DIR los archivos guardados con el formato especificado en FC_TIME_FORMAT como nombre
def filecopy():
	return


#Realiza la copia binaria del disco entero, es mas lenta pero copia toda la información incluso la borrada y no sobreescrita
#Guarda en DD_SAVE_DIR la copia binaria en formato iso con el formato especificado en DD_TIME_FORMAT como nombre
def ddcopy():
    call(['dd','if=/dev/disk/by-path/'+file,'of='+settings.DD_SAVE_DIR+time.strftime('%S:%H-%d-%m-%Y',time.gmtime())+'.iso'])

while True:
    os.chdir('/dev/disk/by-path') #directorio donde buscar los discos y particiones
    for file in glob.glob('*[usb]*'): #filtro para solo mostrar los dispositivos usb
        temp_disk.append(file)
        if disks.count(file) == 0:
            disks.append(file) #guardo en una lista cada uno de los archivos
            if 'part' in file: #si el archivo es una partición
                print('PART:\n'+file)
                check_action(file)
            else: #si no es una partición, sino el disco completo
                print('DISK:\n'+file)


            
