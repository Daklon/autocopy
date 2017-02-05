from subprocess import call
import os
import glob
import settings
import time
import re

disks = []
temp_disks = []

def check_action(file):
    results = [s for s in re.split(':',file)] #parte la cadena en campos, usa ":" como separador para obtener el puerto del pendrive
    puerto = results.pop(3)
    print(puerto)
    if puerto == '1':
        if not 'part' in file:
            ddcopy(file)
    elif puerto == '2':
        filecopy(file)

#Realiza la copia de ficheros(usa la partición, no el disco), es mas rápida que el dd pero a costa de copiar menos información
#Guarda en FC_SAVE_DIR los archivos, en una directorio con el formato especificado en FC_TIME_FORMAT como nombre
def filecopy(file):
    call(['mount',file,settings.MOUNT_DIR])
    save_dir = settings.FC_SAVE_DIR+time.strftime(settings.FC_TIME_FORMAT,time.gmtime())
    call(['mkdir',save_dir])
    call(['cp','-R',settings.MOUNT_DIR,save_dir])


#Realiza la copia binaria del disco entero, es mas lenta pero copia toda la información incluso la borrada y no sobreescrita
#Guarda en DD_SAVE_DIR la copia binaria en formato iso con el formato especificado en DD_TIME_FORMAT como nombre
def ddcopy(file):
    call(['dd','if=/dev/disk/by-path/'+file,'of='+settings.DD_SAVE_DIR+time.strftime('%S:%H-%d-%m-%Y',time.gmtime())+'.iso'])

while True:
    os.chdir('/dev/disk/by-path') #directorio donde buscar los discos y particiones
    temp_disks = []
    for file in glob.glob('*[usb]*'): #filtro para solo mostrar los dispositivos usb
        temp_disks.append(file)
        if disks.count(file) == 0:
            disks.append(file) #guardo en una lista cada uno de los archivos
            check_action(file)
    if len(temp_disks) < len(disks): #compruebo si se ha desenchufado algún disco para eliminarlo de la lista
        for file in disks:
            if not file in temp_disks:
                disks.remove(file)
