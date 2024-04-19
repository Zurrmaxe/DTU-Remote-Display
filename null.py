#!/usr/bin/env python3

# for Display:

import requests, time, sys
from requests.auth import HTTPBasicAuth

import math
import os

import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

disp.contrast(255)


# Clear display.
def main():
#  # Setup display
  disp.begin()
  disp.clear()
  disp.display()


width = disp.width
height = disp.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
draw.rectangle((0, 0, width, height), outline=0, fill=0)

def draw_text(text, line=0):
    draw.text((5, 5 + line * 10), text, font=font, fill=1)

font_path = str('/opt/local/fonts/Roboto-Light.ttf')
font12 = ImageFont.truetype(font_path, 12)
font14 = ImageFont.truetype(font_path, 14)
font16 = ImageFont.truetype(font_path, 16)
font20 = ImageFont.truetype(font_path, 20)
font22 = ImageFont.truetype(font_path, 22)
font = ImageFont.truetype(font_path, 18)


# Diese Daten müssen angepasst werden:
serial = "138290780486" # Seriennummer des Hoymiles Wechselrichters
maximum_wr = 2200 # Maximale Ausgabe des Wechselrichters
minimum_wr = 500 # Minimale Ausgabe des Wechselrichters

dtu_ip = '192.168.178.191' # IP Adresse von OpenDTU
dtu_nutzer = 'admin' # OpenDTU Nutzername
dtu_passwort = 'Volzel1990' # OpenDTU Passwort

shelly_ip = '192.168.178.200' # IP Adresse von Shelly 3EM


#msa = grid_sum

def get_ip():
    cmd = "hostname -I | awk '{print $1}'"
    IP = subprocess.check_output(cmd, shell = True ).decode("utf-8")
    return "IP:" + str(IP).rstrip("\r\n")+" "


while True:
    draw.rectangle((0,0,width,height), outline=0,fill=0)
    msg = get_ip()
    power = 0
    altes_limit = 0
    try:
        draw.rectangle((0,0,width,height), outline=0,fill=0)
        r = requests.get(url = f'http://{dtu_ip}/api/livedata/status?inv=138290780486').json()
        # Selektiert spezifische Daten aus der json response
        reachable   = r['inverters'][0]['reachable'] # Ist DTU erreichbar?
        producing   = int(r['inverters'][0]['producing']) # Produziert der Wechselrichter etwas?
        altes_limit = int(r['inverters'][0]['limit_absolute']) # Altes Limit
        power_dc    = r['inverters'][0]['DC']['0']['Power']['v']  # Lieferung DC vom Panel
        power       = r['inverters'][0]['AC']['0']['Power']['v'] # Abgabe BKW AC in Watt
        powerDay    = r['total']['YieldDay']['v'] # Abgabe BKW AC in Watt
        powerYear   = r['total']['YieldTotal']['v'] # Abgabe BKW AC in Watt

    except:
        #print(power)
        #draw.text((2,49),"Fehler DTU ",font=font12, fill=255)
        disp.image(image)
        disp.show()
        print('Fehler beim Abrufen der Daten von openDTU')
    try:
        # Nimmt Daten von der Shelly 3EM Rest-API und übersetzt sie in ein json-Format
        phase_a     = requests.get(f'http://{shelly_ip}/emeter/0', headers={'Content-Type': 'application/json'}).json()['power']
        phase_b     = requests.get(f'http://{shelly_ip}/emeter/1', headers={'Content-Type': 'application/json'}).json()['power']
        phase_c     = requests.get(f'http://{shelly_ip}/emeter/2', headers={'Content-Type': 'application/json'}).json()['power']
        grid_sum    = phase_a + phase_b + phase_c # Aktueller Bezug - rechnet alle Phasen zusammen
    except:
        draw.text((2,50),"Fehler Shelly ",font=font12, fill=255)
        disp.image(image)
        disp.show()
        print('Fehler beim Abrufen der Daten von Shelly 3EM')

    # Werte setzen
    print(f'\nBezug: {round(grid_sum, 1)} W, Produktion: {round(power)} W, Tag: {round(powerDay)} W/h, Jahr: {round(powerYear)} KW,Verbrauch: {round(grid_sum + power)} W')

    if power < 40 :
        draw.rectangle((0,0,width,height), outline=0,fill=0)
        draw.text((0,0),msg,font=font12, fill=255)
        draw.text((0,13),"Tag   :     " + str(powerDay)+ "W/h",font=font12, fill=255)
        draw.text((0,26),"Jahr  :     " + str(round(powerYear))+ "kW",font=font12, fill=255)
    else: 
        #draw.text((0,0),msg,font=font12, fill=255)
        draw.text((0,0), "Solar :     " + str(round(power)),font=font14, fill=255)
        draw.text((0,13),"Netz  :     " + str(round(grid_sum)),font=font14, fill=255)
        draw.text((0,26),"Last  :     " + str(round(grid_sum + power)),font=font14,fill=255)
        #time.sleep(2)
        #draw.text((2,52),"Limit: WR  : " + str(round(altes_limit)),font=font12, fill=255)

    #if reachable:
        #draw.text((0,52),"Solar ist offline  ",font=font12, fill=255)
    #else:
        #draw.text((2,52),"Solar ist online ",font=font12, fill=255)

    if power > 1:
        #draw.text((0,49),"Solaranlage Ein ",font=font12, fill=255)
        os.system("sh /opt/local/Sol_on.sh")
    else:
        os.system("sh /opt/local/Sol_off.sh")
        #draw.text((2,49),"DTU ist aus ",font=font12, fill=255)
        # Fange oberes Limit ab
    if grid_sum > 1:
        print("Es wird Strom verbraucht")
        os.system("sh /opt/local/Bz_off.sh")
        os.system("sh /opt/local/Netz_on.sh")
        draw.text((0,39),"Netz =>  Verbrauch ",font=font12, fill=255)
    elif grid_sum < 0 :
        print("Es wird Strom eingespeist")
        draw.text((0,39),"Netz =>  Einspeisung ",font=font12, fill=255)
        os.system("sh /opt/local/Bz_on.sh")
        os.system("sh /opt/local/Netz_off.sh")
    else:
            print("fehler") 

    if reachable:
        setpoint = grid_sum + altes_limit - 5 # Neues Limit in Watt

        # Fange oberes Limit ab
        if setpoint > maximum_wr:
            setpoint = maximum_wr
            print(f'Setpoint auf Maximum: {maximum_wr} W')
        # Fange unteres Limit ab
        elif setpoint < minimum_wr:
            setpoint = minimum_wr
            print(f'Setpoint auf Minimum: {minimum_wr} W')
        else:
            print(f'Setpoint berechnet: {round(grid_sum, 1)} W + {round(altes_limit, 1)} W - 5 W = {round(setpoint, 1)} W')

        if setpoint != altes_limit:
            print(f'Setze Inverterlimit von {round(altes_limit, 1)} W auf {round(setpoint, 1)} W... ', end='')
            # Neues Limit setzen
            draw.text((2,52),"Limit: WR  : " + str(round(setpoint)),font=font12, fill=255)
            disp.image(image)
            disp.show()

            try:
                r = requests.post(
                    url = f'http://{dtu_ip}/api/limit/config',
                    data = f'data={{"serial":"{serial}", "limit_type":0, "limit_value":{setpoint}}}',
                    auth = HTTPBasicAuth(dtu_nutzer, dtu_passwort),
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                )
                print(f'Konfiguration gesendet ({r.json()["type"]})')

            except:
                ##draw.text((2,39),"TX Error ",font=font12, fill=255)
                ##disp.image(image)
                ##disp.show()
                print('Fehler beim Senden der Konfiguration')

    sys.stdout.flush() # write out cached messages to stdout
    disp.image(image)
    disp.show()
    time.sleep(2) # wait
