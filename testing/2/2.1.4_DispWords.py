import RPi.GPIO as GPIO
import time, json
import numpy as np
from pathlib import Path

# Display size constants
COL = 360
ROW = 360
cursor = []
font = {}

def add_trailing_zero(mat):
    if len(mat) == 16:
        return mat
    trailing_height = 16-len(mat)
    result = np.concatenate((np.full((trailing_height,(len(mat[0]))),0),mat),axis=0)
    print(result.shape)
    return result

def loadFont():
    script_dir = Path(__file__).parent
    file_path = (script_dir / "bitmap.json").resolve()
    with open(file_path, "r") as f:
        global font
        font = json.load(f)
    

def empty_array(color=[0x00,0x00]):
    array = np.full((COL,ROW,2),color) # fill the empty matrix with the color (default is black)
    return array # Note that this is numpy type thing, not just a python list

# SPI write - lowest level data-sending
def spi_write(dat):
    for i in range(8):
        if dat & 0x80:
            GPIO.output(SI0, GPIO.HIGH)
        else:
            GPIO.output(SI0, GPIO.LOW)
        dat <<= 1
        GPIO.output(SCL, GPIO.LOW)
        GPIO.output(SCL, GPIO.HIGH)

# write_cmd - use the spi_write to send data properly
def write_cmd(cmd):
    spi_write(0x02)
    spi_write(0x00)
    spi_write(cmd)
    spi_write(0x00)

# write_dat - EXACT TRANSLATION  
def write_dat(dat):
    spi_write(dat)

# Write the 8 bit data to the SI pins parallel-ly
def write_lcd(dat):
    GPIO.output(SCL, GPIO.LOW)
    
    if dat & 0x80:
        GPIO.output(SI3, GPIO.HIGH)
    else:
        GPIO.output(SI3, GPIO.LOW)
    
    if dat & 0x40:
        GPIO.output(SI2, GPIO.HIGH)
    else:
        GPIO.output(SI2, GPIO.LOW)
    
    if dat & 0x20:
        GPIO.output(SI1, GPIO.HIGH)
    else:
        GPIO.output(SI1, GPIO.LOW)
    
    if dat & 0x10:
        GPIO.output(SI0, GPIO.HIGH)
    else:
        GPIO.output(SI0, GPIO.LOW)
    
    GPIO.output(SCL, GPIO.HIGH)
    GPIO.output(SCL, GPIO.LOW)
    
    if dat & 0x08:
        GPIO.output(SI3, GPIO.HIGH)
    else:
        GPIO.output(SI3, GPIO.LOW)
    
    if dat & 0x04:
        GPIO.output(SI2, GPIO.HIGH)
    else:
        GPIO.output(SI2, GPIO.LOW)
    
    if dat & 0x02:
        GPIO.output(SI1, GPIO.HIGH)
    else:
        GPIO.output(SI1, GPIO.LOW)
    
    if dat & 0x01:
        GPIO.output(SI0, GPIO.HIGH)
    else:
        GPIO.output(SI0, GPIO.LOW)
    
    GPIO.output(SCL, GPIO.HIGH)

# LCD_Init - just copy from official initialization code
def LCD_Init():
    # Reset sequence
    GPIO.output(CS0, GPIO.LOW)
    GPIO.output(RST, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(RST, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(RST, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(CS0, GPIO.HIGH)
    
    # ALL INIT COMMANDS - EXACT AS C CODE
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF0)
    write_dat(0x28)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF2)
    write_dat(0x28)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x73)
    write_dat(0xF0)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x7C)
    write_dat(0xD1)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x83)
    write_dat(0xE0)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x84)
    write_dat(0x61)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF2)
    write_dat(0x82)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF0)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF0)
    write_dat(0x01)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF1)
    write_dat(0x01)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB0)
    write_dat(0x69)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB1)
    write_dat(0x4A)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB2)
    write_dat(0x2F)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB3)
    write_dat(0x01)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB4)
    write_dat(0x69)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB5)
    write_dat(0x45)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB6)
    write_dat(0xAB)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB7)
    write_dat(0x41)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB8)
    write_dat(0x86)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB9)
    write_dat(0x15)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBA)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBB)
    write_dat(0x08)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBC)
    write_dat(0x08)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBD)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBE)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBF)
    write_dat(0x07)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC0)
    write_dat(0x80)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC1)
    write_dat(0x10)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC2)
    write_dat(0x37)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC3)
    write_dat(0x80)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC4)
    write_dat(0x10)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC5)
    write_dat(0x37)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC6)
    write_dat(0xA9)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC7)
    write_dat(0x41)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC8)
    write_dat(0x01)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC9)
    write_dat(0xA9)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xCA)
    write_dat(0x41)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xCB)
    write_dat(0x01)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xCC)
    write_dat(0x7F)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xCD)
    write_dat(0x7F)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xCE)
    write_dat(0xFF)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD0)
    write_dat(0x91)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD1)
    write_dat(0x68)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD2)
    write_dat(0x68)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF5)
    write_dat(0x00)
    write_dat(0xA5)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF1)
    write_dat(0x10)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF0)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF0)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE0)
    write_dat(0xF0)
    write_dat(0x10)
    write_dat(0x18)
    write_dat(0x0D)
    write_dat(0x0C)
    write_dat(0x38)
    write_dat(0x3E)
    write_dat(0x44)
    write_dat(0x51)
    write_dat(0x39)
    write_dat(0x15)
    write_dat(0x15)
    write_dat(0x30)
    write_dat(0x34)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE1)
    write_dat(0xF0)
    write_dat(0x0F)
    write_dat(0x17)
    write_dat(0x0D)
    write_dat(0x0B)
    write_dat(0x07)
    write_dat(0x3E)
    write_dat(0x33)
    write_dat(0x51)
    write_dat(0x39)
    write_dat(0x15)
    write_dat(0x15)
    write_dat(0x30)
    write_dat(0x34)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF0)
    write_dat(0x10)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF3)
    write_dat(0x10)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE0)
    write_dat(0x08)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE1)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE2)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE3)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE4)
    write_dat(0xE0)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE5)
    write_dat(0x06)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE6)
    write_dat(0x21)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE7)
    write_dat(0x03)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE8)
    write_dat(0x05)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xE9)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xEA)
    write_dat(0xE9)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xEB)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xEC)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xED)
    write_dat(0x14)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xEE)
    write_dat(0xFF)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xEF)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF8)
    write_dat(0xFF)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF9)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xFA)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xFB)
    write_dat(0x30)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xFC)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xFD)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xFE)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xFF)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x60)
    write_dat(0x40)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x61)
    write_dat(0x05)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x62)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x63)
    write_dat(0x42)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x64)
    write_dat(0xDA)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x65)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x66)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x67)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x68)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x69)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x6A)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x6B)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x70)
    write_dat(0x40)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x71)
    write_dat(0x04)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x72)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x73)
    write_dat(0x42)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x74)
    write_dat(0xD9)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x75)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x76)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x77)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x78)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x79)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x7A)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x7B)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x80)
    write_dat(0x48)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x81)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x82)
    write_dat(0x07)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x83)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x84)
    write_dat(0xD7)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x85)
    write_dat(0x04)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x86)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x87)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x88)
    write_dat(0x48)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x89)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x8A)
    write_dat(0x09)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x8B)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x8C)
    write_dat(0xD9)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x8D)
    write_dat(0x04)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x8E)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x8F)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x90)
    write_dat(0x48)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x91)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x92)
    write_dat(0x0B)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x93)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x94)
    write_dat(0xDB)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x95)
    write_dat(0x04)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x96)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x97)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x98)
    write_dat(0x48)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x99)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x9A)
    write_dat(0x0D)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x9B)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x9C)
    write_dat(0xDD)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x9D)
    write_dat(0x04)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x9E)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x9F)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA0)
    write_dat(0x48)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA1)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA2)
    write_dat(0x06)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA3)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA4)
    write_dat(0xD6)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA5)
    write_dat(0x04)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA6)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA7)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA8)
    write_dat(0x48)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xA9)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xAA)
    write_dat(0x08)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xAB)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xAC)
    write_dat(0xD8)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xAD)
    write_dat(0x04)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xAE)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xAF)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB0)
    write_dat(0x48)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB1)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB2)
    write_dat(0x0A)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB3)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB4)
    write_dat(0xDA)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB5)
    write_dat(0x04)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB6)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB7)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB8)
    write_dat(0x48)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xB9)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBA)
    write_dat(0x0C)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBB)
    write_dat(0x02)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBC)
    write_dat(0xDC)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBD)
    write_dat(0x04)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBE)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xBF)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC0)
    write_dat(0x10)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC1)
    write_dat(0x47)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC2)
    write_dat(0x56)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC3)
    write_dat(0x65)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC4)
    write_dat(0x74)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC5)
    write_dat(0x88)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC6)
    write_dat(0x99)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC7)
    write_dat(0x01)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC8)
    write_dat(0xBB)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xC9)
    write_dat(0xAA)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD0)
    write_dat(0x10)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD1)
    write_dat(0x47)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD2)
    write_dat(0x56)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD3)
    write_dat(0x65)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD4)
    write_dat(0x74)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD5)
    write_dat(0x88)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD6)
    write_dat(0x99)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD7)
    write_dat(0x01)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD8)
    write_dat(0xBB)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xD9)
    write_dat(0xAA)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF3)
    write_dat(0x01)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0xF0)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x3A)
    write_dat(0x05)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x35)
    write_dat(0x00)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x21)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x11)
    GPIO.output(CS0, GPIO.HIGH)
    
    time.sleep(0.12)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x29)
    GPIO.output(CS0, GPIO.HIGH)
    
    GPIO.output(CS0, GPIO.LOW)
    write_cmd(0x2C)
    GPIO.output(CS0, GPIO.HIGH)

# DispColorQSPI - Translated official C code to python
def DispColorQSPI(data1, data2):
    GPIO.output(CS0, GPIO.LOW)
    
    spi_write(0x12)
    write_lcd(0x00)
    write_lcd(0x2C)
    write_lcd(0x00)
    
    for i in range(ROW):
        for j in range(COL):
            write_lcd(data1)
            write_lcd(data2)
    
    GPIO.output(CS0, GPIO.HIGH)

# Display a matrix of pixels
def DispPixels(mat): # Parse in Numpy arrays pls
    '''It's shape should be (rows,columns,2), for example
    [
        [[0xff,0xe0],[0xa0,0x55]],
        [[0x67,0x76],[0x12,0x34]],
        [[0x56,0x78],[0x89,0x9a]]
    ]
    Above is a image with six pixels, with three rows and two columns
    '''
    print("Displaying")
    # Just configs/inits based on the given example code
    GPIO.output(CS0, GPIO.LOW)
    spi_write(0x12)
    write_lcd(0x00)
    write_lcd(0x2C)
    write_lcd(0x00)

    #Write the pixels according to the matrix
    for row in mat:
        for pixel in row:
            write_lcd(pixel[0])
            write_lcd(pixel[1])
    GPIO.output(CS0, GPIO.HIGH)

def BlockWrite(dim):
    Xstart, Xend, Ystart, Yend = dim
    GPIO.output(CS0,GPIO.LOW)
    write_cmd(0x2a)
    write_dat(Xstart>>8)
    write_dat(Xstart)
    write_dat(Xend>>8)
    write_dat(Xend)
    GPIO.output(CS0,GPIO.HIGH)

    GPIO.output(CS0,GPIO.LOW)
    write_cmd(0x2b)
    write_dat(Ystart>>8)
    write_dat(Ystart)
    write_dat(Yend>>8)
    write_dat(Yend)
    GPIO.output(CS0,GPIO.HIGH)

    GPIO.output(CS0,GPIO.LOW)
    write_cmd(0x2c)
    GPIO.output(CS0,GPIO.HIGH)

def DispPixels_fast(mat,dim, bg_color,font_color):
    '''dim = (Xstart,Xend,Ystart,Yend)'''
    BlockWrite(dim) # Selection the area that u wanna write, with a tuple with 4 items

    GPIO.output(CS0,GPIO.LOW)
    spi_write(0x12)
    write_lcd(0x00)
    write_lcd(0x2C)
    write_lcd(0x00)

    for row in mat:
        for pixel in row:
            if pixel:
                write_lcd(font_color[0])
                write_lcd(font_color[1])
            else:
                write_lcd(bg_color[0])
                write_lcd(bg_color[1])
    GPIO.output(CS0, GPIO.HIGH)

def generateDim(mat_size):
    '''mat_size=(columns, rows)'''
    return [cursor[0],cursor[0]+mat_size[0]-1, cursor[1], cursor[1] + mat_size[1]-1]

def DispLetter(letter, bg_color,font_color,dim=None): 
    '''Only accepts a letter, not a word'''
    if not dim:
        dim = generateDim(len(letter[0]),len(letter))
    if not font:
        loadFont()
    letter_mat = font[letter]
    DispPixels_fast(letter_mat,dim,bg_color,font_color)

def dispWord(word, bg_color, font_color, dim=None):
    '''Accepts a word, doesn't change lines by itself'''
    if not font:
        loadFont()
    word_mat = np.full((16,0),0)
    print(word)
    for i in range(len(word)):
        letter = add_trailing_zero(font[word[i]])
        word_mat = np.concatenate((word_mat,letter),axis=1)
    print(word_mat)
    DispPixels_fast(word_mat,generateDim((len(word_mat[0]),len(word_mat))),bg_color,font_color)
def DispBlock(data1,data2):
    BlockWrite(100,139,100,139)

    GPIO.output(CS0,GPIO.LOW)
    spi_write(0x12)
    write_lcd(0x00)
    write_lcd(0x2C)
    write_lcd(0x00)
    for i in range(40):
        for j in range(40):
            write_lcd(data1)
            write_lcd(data2)


# Test function
def test_display():
    print("Initializing GPIO...")
    
    # SET THESE TO YOUR ACTUAL PIN NUMBERS!
    global SI0, SI1, SI2, SI3, SCL, CS0, RST, BL
    
    # Example pins - YOU MUST CHANGE THESE!
    SI0 = 10   # GPIO 10 - Physical pin 19
    SI1 = 22    # GPIO 9  - Physical pin 21
    SI2 = 27   # GPIO 11 - Physical pin 23
    SI3 = 17    # GPIO 8  - Physical pin 24
    SCL = 11    # GPIO 7  - Physical pin 26
    CS0 = 5    # GPIO 5  - Physical pin 29
    RST = 25   # GPIO 25 - Physical pin 22
    BL = 16    # GPIO 16 - Physical pin 36
    
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    for pin in [SI0, SI1, SI2, SI3, SCL, CS0, RST, BL]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    # Turn on backlight
    GPIO.output(BL, GPIO.HIGH)
    
    print("Initializing display...")
    time.sleep(4)
    LCD_Init()
    print("init complete")
    global cursor
    DispColorQSPI(0xe8,0x00)
    cursor = [100,180]
    
    dispWord(
        "Good morning",
        bg_color = (0xe8,0x00), # Red
        font_color = (0xff,0xe0) # Yellow
    )
    wait = input("Enter sth when finish")    
    print("Test complete")

if __name__ == "__main__":
    try:
        test_display()
        GPIO.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        GPIO.cleanup()
    finally:
        GPIO.cleanup()