from picounicorn import PicoUnicorn
import time
import utime
import machine
import random
picounicorn = PicoUnicorn()
rtc = machine.RTC()
pixels = [
    0x00, 0x00, 0x00, 0x00, 0x00,  # 0x00 (nul)
    0x3E, 0x5B, 0x4F, 0x5B, 0x3E,  # 0x01 (soh)
    0x3E, 0x6B, 0x4F, 0x6B, 0x3E,  # 0x02 (stx)
    0x1C, 0x3E, 0x7C, 0x3E, 0x1C,  # 0x03 (etx)
    0x18, 0x3C, 0x7E, 0x3C, 0x18,  # 0x04 (eot)
    0x1C, 0x57, 0x7D, 0x57, 0x1C,  # 0x05 (enq)
    0x1C, 0x5E, 0x7F, 0x5E, 0x1C,  # 0x06 (ack)
    0x00, 0x18, 0x3C, 0x18, 0x00,  # 0x07 (bel)
    0xFF, 0xE7, 0xC3, 0xE7, 0xFF,  # 0x08 (bs)
    0x00, 0x18, 0x24, 0x18, 0x00,  # 0x09 (tab)
    0xFF, 0xE7, 0xDB, 0xE7, 0xFF,  # 0x0A (lf)
    0x30, 0x48, 0x3A, 0x06, 0x0E,  # 0x0B (vt)
    0x26, 0x29, 0x79, 0x29, 0x26,  # 0x0C (np)
    0x40, 0x7F, 0x05, 0x05, 0x07,  # 0x0D (cr)
    0x40, 0x7F, 0x05, 0x25, 0x3F,  # 0x0E (so)
    0x5A, 0x3C, 0xE7, 0x3C, 0x5A,  # 0x0F (si)
    0x7F, 0x3E, 0x1C, 0x1C, 0x08,  # 0x10 (dle)
    0x08, 0x1C, 0x1C, 0x3E, 0x7F,  # 0x11 (dc1)
    0x14, 0x22, 0x7F, 0x22, 0x14,  # 0x12 (dc2)
    0x5F, 0x5F, 0x00, 0x5F, 0x5F,  # 0x13 (dc3)
    0x06, 0x09, 0x7F, 0x01, 0x7F,  # 0x14 (dc4)
    0x00, 0x66, 0x89, 0x95, 0x6A,  # 0x15 (nak)
    0x60, 0x60, 0x60, 0x60, 0x60,  # 0x16 (syn)
    0x94, 0xA2, 0xFF, 0xA2, 0x94,  # 0x17 (etb)
    0x08, 0x04, 0x7E, 0x04, 0x08,  # 0x18 (can)
    0x10, 0x20, 0x7E, 0x20, 0x10,  # 0x19 (em)
    0x08, 0x08, 0x2A, 0x1C, 0x08,  # 0x1A (eof)
    0x08, 0x1C, 0x2A, 0x08, 0x08,  # 0x1B (esc)
    0x1E, 0x10, 0x10, 0x10, 0x10,  # 0x1C (fs)
    0x0C, 0x1E, 0x0C, 0x1E, 0x0C,  # 0x1D (gs)
    0x30, 0x38, 0x3E, 0x38, 0x30,  # 0x1E (rs)
    0x06, 0x0E, 0x3E, 0x0E, 0x06,  # 0x1F (us)
    0x00, 0x00, 0x00, 0x00, 0x00,  # 0x20
    0x00, 0x00, 0x5F, 0x00, 0x00,  # 0x21 !
    0x00, 0x07, 0x00, 0x07, 0x00,  # 0x22 "
    0x14, 0x7F, 0x14, 0x7F, 0x14,  # 0x23 #
    0x24, 0x2A, 0x7F, 0x2A, 0x12,  # 0x24 $
    0x23, 0x13, 0x08, 0x64, 0x62,  # 0x25 %
    0x36, 0x49, 0x56, 0x20, 0x50,  # 0x26 &
    0x00, 0x08, 0x07, 0x03, 0x00,  # 0x27 '
    0x00, 0x1C, 0x22, 0x41, 0x00,  # 0x28 (
    0x00, 0x41, 0x22, 0x1C, 0x00,  # 0x29 )
    0x2A, 0x1C, 0x7F, 0x1C, 0x2A,  # 0x2A *
    0x08, 0x08, 0x3E, 0x08, 0x08,  # 0x2B +
    0x00, 0x80, 0x70, 0x30, 0x00,  # 0x2C ,
    0x08, 0x08, 0x08, 0x08, 0x08,  # 0x2D -
    0x00, 0x00, 0x60, 0x60, 0x00,  # 0x2E .
    0x20, 0x10, 0x08, 0x04, 0x02,  # 0x2F /
    0x3E, 0x51, 0x49, 0x45, 0x3E,  # 0x30 0
    0x00, 0x42, 0x7F, 0x40, 0x00,  # 0x31 1
    0x72, 0x49, 0x49, 0x49, 0x46,  # 0x32 2
    0x21, 0x41, 0x49, 0x4D, 0x33,  # 0x33 3
    0x18, 0x14, 0x12, 0x7F, 0x10,  # 0x34 4
    0x27, 0x45, 0x45, 0x45, 0x39,  # 0x35 5
    0x3C, 0x4A, 0x49, 0x49, 0x31,  # 0x36 6
    0x41, 0x21, 0x11, 0x09, 0x07,  # 0x37 7
    0x36, 0x49, 0x49, 0x49, 0x36,  # 0x38 8
    0x46, 0x49, 0x49, 0x29, 0x1E,  # 0x39 9
    0x00, 0x00, 0x14, 0x00, 0x00,  # 0x3A :
    0x3C, 0x26, 0x23, 0x26, 0x3C,  # 0x7F
    0x1E, 0xA1, 0xA1, 0x61, 0x12,  # 0x80
    0x3A, 0x40, 0x40, 0x20, 0x7A,  # 0x81
    0x38, 0x54, 0x54, 0x55, 0x59,  # 0x82
    0x21, 0x55, 0x55, 0x79, 0x41,  # 0x83
    0x22, 0x54, 0x54, 0x78, 0x42,  # 0x84
    0x21, 0x55, 0x54, 0x78, 0x40,  # 0x85
    0x20, 0x54, 0x55, 0x79, 0x40,  # 0x86
    0x0C, 0x1E, 0x52, 0x72, 0x12,  # 0x87
    0x39, 0x55, 0x55, 0x55, 0x59,  # 0x88
    0x39, 0x54, 0x54, 0x54, 0x59,  # 0x89
    0x39, 0x55, 0x54, 0x54, 0x58,  # 0x8A
    0x00, 0x00, 0x45, 0x7C, 0x41,  # 0x8B
    0x00, 0x02, 0x45, 0x7D, 0x42,  # 0x8C
    0x00, 0x01, 0x45, 0x7C, 0x40,  # 0x8D
    0x7D, 0x12, 0x11, 0x12, 0x7D,  # 0x8E
    0xF0, 0x28, 0x25, 0x28, 0xF0,  # 0x8F
    0x7C, 0x54, 0x55, 0x45, 0x00,  # 0x90
    0x20, 0x54, 0x54, 0x7C, 0x54,  # 0x91
    0x7C, 0x0A, 0x09, 0x7F, 0x49,  # 0x92
    0x32, 0x49, 0x49, 0x49, 0x32,  # 0x93
    0x3A, 0x44, 0x44, 0x44, 0x3A,  # 0x94
    0x32, 0x4A, 0x48, 0x48, 0x30,  # 0x95
    0x3A, 0x41, 0x41, 0x21, 0x7A,  # 0x96
    0x3A, 0x42, 0x40, 0x20, 0x78,  # 0x97
    0x00, 0x9D, 0xA0, 0xA0, 0x7D,  # 0x98
    0x3D, 0x42, 0x42, 0x42, 0x3D,  # 0x99
    0x3D, 0x40, 0x40, 0x40, 0x3D,  # 0x9A
    0x3C, 0x24, 0xFF, 0x24, 0x24,  # 0x9B
    0x48, 0x7E, 0x49, 0x43, 0x66,  # 0x9C
    0x2B, 0x2F, 0xFC, 0x2F, 0x2B,  # 0x9D
    0xFF, 0x09, 0x29, 0xF6, 0x20,  # 0x9E
    0xC0, 0x88, 0x7E, 0x09, 0x03,  # 0x9F
    0x20, 0x54, 0x54, 0x79, 0x41,  # 0xA0
    0x00, 0x00, 0x44, 0x7D, 0x41,  # 0xA1
    0x30, 0x48, 0x48, 0x4A, 0x32,  # 0xA2
    0x38, 0x40, 0x40, 0x22, 0x7A,  # 0xA3
    0x00, 0x7A, 0x0A, 0x0A, 0x72,  # 0xA4
    0x7D, 0x0D, 0x19, 0x31, 0x7D,  # 0xA5
    0x26, 0x29, 0x29, 0x2F, 0x28,  # 0xA6
    0x26, 0x29, 0x29, 0x29, 0x26,  # 0xA7
    0x30, 0x48, 0x4D, 0x40, 0x20,  # 0xA8
    0x38, 0x08, 0x08, 0x08, 0x08,  # 0xA9
    0x08, 0x08, 0x08, 0x08, 0x38,  # 0xAA
    0x2F, 0x10, 0xC8, 0xAC, 0xBA,  # 0xAB
    0x2F, 0x10, 0x28, 0x34, 0xFA,  # 0xAC
    0x00, 0x00, 0x7B, 0x00, 0x00,  # 0xAD
    0x08, 0x14, 0x2A, 0x14, 0x22,  # 0xAE
    0x22, 0x14, 0x2A, 0x14, 0x08,  # 0xAF
    0x55, 0x00, 0x55, 0x00, 0x55,  # 0xB0
    0xAA, 0x55, 0xAA, 0x55, 0xAA,  # 0xB1
    0xFF, 0x55, 0xFF, 0x55, 0xFF,  # 0xB2
    0x00, 0x00, 0x00, 0xFF, 0x00,  # 0xB3
    0x10, 0x10, 0x10, 0xFF, 0x00,  # 0xB4
    0x14, 0x14, 0x14, 0xFF, 0x00,  # 0xB5
    0x10, 0x10, 0xFF, 0x00, 0xFF,  # 0xB6
    0x10, 0x10, 0xF0, 0x10, 0xF0,  # 0xB7
    0x14, 0x14, 0x14, 0xFC, 0x00,  # 0xB8
    0x14, 0x14, 0xF7, 0x00, 0xFF,  # 0xB9
    0x00, 0x00, 0xFF, 0x00, 0xFF,  # 0xBA
    0x14, 0x14, 0xF4, 0x04, 0xFC,  # 0xBB
    0x14, 0x14, 0x17, 0x10, 0x1F,  # 0xBC
    0x10, 0x10, 0x1F, 0x10, 0x1F,  # 0xBD
    0x14, 0x14, 0x14, 0x1F, 0x00,  # 0xBE
    0x10, 0x10, 0x10, 0xF0, 0x00,  # 0xBF
    0x00, 0x00, 0x00, 0x1F, 0x10,  # 0xC0
    0x10, 0x10, 0x10, 0x1F, 0x10,  # 0xC1
    0x10, 0x10, 0x10, 0xF0, 0x10,  # 0xC2
    0x00, 0x00, 0x00, 0xFF, 0x10,  # 0xC3
    0x10, 0x10, 0x10, 0x10, 0x10,  # 0xC4
    0x10, 0x10, 0x10, 0xFF, 0x10,  # 0xC5
    0x00, 0x00, 0x00, 0xFF, 0x14,  # 0xC6
    0x00, 0x00, 0xFF, 0x00, 0xFF,  # 0xC7
    0x00, 0x00, 0x1F, 0x10, 0x17,  # 0xC8
    0x00, 0x00, 0xFC, 0x04, 0xF4,  # 0xC9
    0x14, 0x14, 0x17, 0x10, 0x17,  # 0xCA
    0x14, 0x14, 0xF4, 0x04, 0xF4,  # 0xCB
    0x00, 0x00, 0xFF, 0x00, 0xF7,  # 0xCC
    0x14, 0x14, 0x14, 0x14, 0x14,  # 0xCD
    0x14, 0x14, 0xF7, 0x00, 0xF7,  # 0xCE
    0x14, 0x14, 0x14, 0x17, 0x14,  # 0xCF
    0x10, 0x10, 0x1F, 0x10, 0x1F,  # 0xD0
    0x14, 0x14, 0x14, 0xF4, 0x14,  # 0xD1
    0x10, 0x10, 0xF0, 0x10, 0xF0,  # 0xD2
    0x00, 0x00, 0x1F, 0x10, 0x1F,  # 0xD3
    0x00, 0x00, 0x00, 0x1F, 0x14,  # 0xD4
    0x00, 0x00, 0x00, 0xFC, 0x14,  # 0xD5
    0x00, 0x00, 0xF0, 0x10, 0xF0,  # 0xD6
    0x10, 0x10, 0xFF, 0x10, 0xFF,  # 0xD7
    0x14, 0x14, 0x14, 0xFF, 0x14,  # 0xD8
    0x10, 0x10, 0x10, 0x1F, 0x00,  # 0xD9
    0x00, 0x00, 0x00, 0xF0, 0x10,  # 0xDA
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF,  # 0xDB
    0xF0, 0xF0, 0xF0, 0xF0, 0xF0,  # 0xDC
    0xFF, 0xFF, 0xFF, 0x00, 0x00,  # 0xDD
    0x00, 0x00, 0x00, 0xFF, 0xFF,  # 0xDE
    0x0F, 0x0F, 0x0F, 0x0F, 0x0F,  # 0xDF
    0x38, 0x44, 0x44, 0x38, 0x44,  # 0xE0
    0xFC, 0x4A, 0x4A, 0x4A, 0x34,  # 0xE1
    0x7E, 0x02, 0x02, 0x06, 0x06,  # 0xE2
    0x02, 0x7E, 0x02, 0x7E, 0x02,  # 0xE3
    0x63, 0x55, 0x49, 0x41, 0x63,  # 0xE4
    0x38, 0x44, 0x44, 0x3C, 0x04,  # 0xE5
    0x40, 0x7E, 0x20, 0x1E, 0x20,  # 0xE6
    0x06, 0x02, 0x7E, 0x02, 0x02,  # 0xE7
    0x99, 0xA5, 0xE7, 0xA5, 0x99,  # 0xE8
    0x1C, 0x2A, 0x49, 0x2A, 0x1C,  # 0xE9
    0x4C, 0x72, 0x01, 0x72, 0x4C,  # 0xEA
    0x30, 0x4A, 0x4D, 0x4D, 0x30,  # 0xEB
    0x30, 0x48, 0x78, 0x48, 0x30,  # 0xEC
    0xBC, 0x62, 0x5A, 0x46, 0x3D,  # 0xED
    0x3E, 0x49, 0x49, 0x49, 0x00,  # 0xEE
    0x7E, 0x01, 0x01, 0x01, 0x7E,  # 0xEF
    0x2A, 0x2A, 0x2A, 0x2A, 0x2A,  # 0xF0
    0x44, 0x44, 0x5F, 0x44, 0x44,  # 0xF1
    0x40, 0x51, 0x4A, 0x44, 0x40,  # 0xF2
    0x40, 0x44, 0x4A, 0x51, 0x40,  # 0xF3
    0x00, 0x00, 0xFF, 0x01, 0x03,  # 0xF4
    0xE0, 0x80, 0xFF, 0x00, 0x00,  # 0xF5
    0x08, 0x08, 0x6B, 0x6B, 0x08,  # 0xF6
    0x36, 0x12, 0x36, 0x24, 0x36,  # 0xF7
    0x06, 0x0F, 0x09, 0x0F, 0x06,  # 0xF8
    0x00, 0x00, 0x18, 0x18, 0x00,  # 0xF9
    0x00, 0x00, 0x10, 0x10, 0x00,  # 0xFA
    0x30, 0x40, 0xFF, 0x01, 0x01,  # 0xFB
    0x00, 0x1F, 0x01, 0x01, 0x1E,  # 0xFC
    0x00, 0x19, 0x1D, 0x17, 0x12,  # 0xFD
    0x00, 0x3C, 0x3C, 0x3C, 0x3C,  # 0xFE
    0x00, 0x00, 0x00, 0x00, 0x00   # 0xFF
]


def display_text(text, r, g, b):
    for x in range(w):
        for y in range(h):
            picounicorn.set_pixel(x, y, 0, 0, 0)

    for i, char in enumerate(text):
        #print(i, char)
        line = ord(char) * 5
        for x in range(5):
            row = pixels[line + x]
            bins = f"{row:#010b}"[3:]
            #print(bins)
            for y in range(7):
                picounicorn.set_pixel(x + (i * 5), y, int(bins[6 - y] or 0) * r, int(bins[6 - y] or 0)* g, int(bins[6 - y] or 0) * b)

w = picounicorn.get_width()
h = picounicorn.get_height()
timestamp = rtc.datetime()
timestring="%02d:%02d"%(timestamp[4:6])
hour = timestamp[4]
minute = timestamp[5]
second = timestamp[6]
print(hour, minute, second)
while True:
    r = random.randint(10,30)
    g = random.randint(10,30)
    b = random.randint(10,30)
    timestamp = rtc.datetime()
    timestring="%02d:%02d"%(timestamp[4:6])
    hour = timestamp[4]
    minute = timestamp[5]
    second = timestamp[6]
    hour1 = hour - 12
    hour12 = 12
    print(hour, minute, second)
    
    if(hour <= 12):
        hour = hour
    else:
        hour = abs(int(hour)) - 12
    if(minute == 0 or minute == 1 or minute == 2 or minute == 3 or minute == 4 or minute == 5 or minute == 6 or minute == 7 or minute == 8 or minute == 9):
        minute = "0" + str(minute);
    if(hour <= 9):
        display_text(f"{hour}{minute}", r, g, b)
        time.sleep(30)
    else:
        display_text(f"{hour}", r, g, b)
        time.sleep(15)
        display_text(f" {minute}", r, g, b)
        time.sleep(15)
    


