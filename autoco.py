# -*- coding:utf-8 -*-
import re
import os
import glob
import time
import settings
import RPi.GPIO as GPIO
from subprocess import call


def on_led(number):
    GPIO.output(number, GPIO.HIGH)


def off_led(number):
    GPIO.output(number, GPIO.LOW)


def check_action(file):
    on_led(17)
# parte la cadena en campos
# usa ":" como separador para obtener el puerto del pendrive
    results = [s for s in re.split(':', file)]
    if settings.DEBUG:
        print("comprobando dispositivos: " + str(results))
    try:
        puerto = results.pop(settings.POP_INDEX)
        if puerto == '1.2':
            if settings.DEBUG:
                print("Detectado puerto 1.2")
            if not 'part' in file:
                if settings.DEBUG:
                    print("ddcopy by 1.2")
                ddcopy(file)
        elif puerto == '1.3':
            if settings.DEBUG:
                print("Detectado 1.3")
            if 'part' in file:
                if settings.DEBUG:
                    print("filecopy by 1.3")
                filecopy(file)
        elif puerto == '1.4':
            if settings.DEBUG:
                print("Detectado puerto 1.4")
            plant(file)
    except Exception as e:
        print("[ERROR] " + str(e.message))
    off_led(17)

# Realiza la copia de ficheros(usa la partición, no el disco),
# es mas rápida que el dd pero a costa de copiar menos información
# Guarda en FC_SAVE_DIR los archivos, en una directorio con
# el formato especificado en FC_TIME_FORMAT como nombre


def filecopy(file):
    on_led(22)
    call(['umount', settings.MOUNT_DIR])
    call(['mount', file, settings.MOUNT_DIR])
    save_dir = settings.FC_SAVE_DIR+time.strftime(settings.FC_TIME_FORMAT, time.gmtime())
    call(['mkdir', save_dir])
    call(['cp', '-R', settings.MOUNT_DIR, save_dir])
    call(['umount', settings.MOUNT_DIR])
    off_led(22)

# Copia de un dir especificado en PLANT_LOAD_DIR a el disco enchufado
# en la ruta PLANT_SAVE_DIR respecto de la raiz del disco,
# luego lo borra, para dejar pruebas forenses


def plant(file):
    on_led(22)
    call(['umount', settings.MOUNT_DIR])
    call(['mount', file, settings.MOUNT_DIR])
    call(['mkdir', settings.MOUNT_DIR+settings.PLANT_SAVE_DIR])
    call(['cp -R', settings.PLANT_LOAD_DIR, settings.MOUNT_DIR+settings.PLANT_SAVE_DIR])
    call(['rm -R', settings.MOUNT_DIR+settings.PLANT_SAVE_DIR])
    call(['umount', settings.MOUNT_DIR])

# Realiza la copia binaria del disco entero, es mas lenta pero copia toda la
# información incluso la borrada y no sobreescrita
# Guarda en DD_SAVE_DIR la copia binaria en formato iso con el formato 
# especificado en DD_TIME_FORMAT como nombre


def ddcopy(file):
    on_led(22)
    command = 'dd if=/dev/disk/by-path/' + file + ' of=' + settings.DD_SAVE_DIR + time.strftime(settings.D_TIME_FORMAT, time.gmtime()) + '.iso'
    if settings.DEBUG:
        print("command:" + command)
    call(command.split(" "))
    off_led(22)


def main():
    disks = []
    temp_disks = []

    # LED CONFIG
    if settings.DEBUG:
        print("Configuración de leds")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)

    off_led(17)
    off_led(21)
    off_led(22)
    off_led(23)
    off_led(24)

    if settings.DEBUG:
        print("Iniciando autoco.py")

    while True:
        # Directorio donde buscar los discos y particiones
        os.chdir('/dev/disk/by-path')
        temp_disks = []
        # Filtro para solo mostrar los dispositivos usb
        for file in glob.glob('*[usb]*'):
            temp_disks.append(file)
            if disks.count(file) == 0:
                if settings.DEBUG:
                    print("Procesando:" + str(file))
        # Guardo en una lista cada uno de los archivos
                disks.append(file)
                check_action(file)
        # Compruebo si se ha desenchufado algún disco
        # para eliminarlo de la lista
        if len(temp_disks) < len(disks):
            for file in disks:
                if not file in temp_disks:
                    disks.remove(file)
