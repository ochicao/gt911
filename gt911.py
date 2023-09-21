# driver para touch gt911 da ESP32-3248S035C
from machine import Pin as GPIO
import time

global GTP_REG_VERSION
GTP_REG_VERSION = 0x8140

global GTP_READ_COOR_ADDR
GTP_READ_COOR_ADDR = 0x814E

#define GTP_REG_SLEEP         0x8040
#define GTP_REG_SENSOR_ID     0x814A
#define GTP_REG_CONFIG_DATA   0x8047
#define GTP_REG_VERSION       0x8140


global rcvbuf
rcvbuf = 0
global xc
xc = 0
global yc
yc = 0

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(13, GPIO.OUT)
p13=GPIO(33, GPIO.OUT)#era 13
p15=GPIO(32, GPIO.OUT)#era 15
p37=GPIO(21, GPIO.OUT)#era 37
p22=GPIO(25, GPIO.OUT)#era 22

def RES_HI():
    #GPIO.output(22, True)
    p22.value(True)

def RES_LO():
    #GPIO.output(22, False)
    p22.value(False)

def INT_HI():
    #GPIO.output(37, True)
    p37.value(True)

def INT_LO():
    #GPIO.output(37, False)
    p37.value(False)

def SCL_HI():
    #GPIO.output(15, True)
    p15.value(True)


def SCL_LO():
    #GPIO.output(15, False)
    p15.value(False)


def SDA_LO():
    #GPIO.output(13, False)
    p13.value(False)

def SDA_HI():
    #GPIO.output(13, True)
    p13.value(True)

def SDA_OUT():
    #GPIO.setup(13, GPIO.OUT)
    p13=GPIO(33, GPIO.OUT)#era 13
    
def SCL_OUT():
    #GPIO.setup(15, GPIO.OUT)
    p15=GPIO(32, GPIO.OUT)#era 15

def SDA_INPUT():
    #GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    p13=GPIO(33, GPIO.IN, GPIO.PULL_UP)#era 13

def SCL_INPUT():
    #GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    p15=GPIO(32, GPIO.IN, GPIO.PULL_UP)#era 15

def INT_INPUT():
    #GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #p13=GPIO(33, GPIO.OUT)#era 13
    #p15=GPIO(32, GPIO.OUT)#era 15
    p37=GPIO(21, GPIO.IN, GPIO.PULL_UP)#era 37
    #p22=GPIO(25, GPIO.OUT)#era 22

def i2c_start():
    SDA_OUT()
    
    SDA_HI()
    time.sleep(0.00001)
    SCL_HI()
    time.sleep(0.00002)
    SDA_LO()
    time.sleep(0.00001)
    SCL_LO()
    
def i2c_stop():
    SDA_OUT()
    
    SDA_LO()
    time.sleep(0.00001)
    SCL_HI()
    time.sleep(0.00002)
    SDA_HI()	
    time.sleep(0.00001)
    #SCL_LO()

def i2c_receive1(aknak):
    data = 0
    mask = 128
    
    SDA_OUT()
    time.sleep(0.001)
    SDA_HI()
    time.sleep(0.001)
    SCL_HI()
    time.sleep(0.001)
    SCL_LO()
    
    SDA_INPUT()
    time.sleep(0.001)
    
    while mask:
        time.sleep(0.001)
        SCL_HI()
        time.sleep(0.001)
        SCL_LO()
        
        #if (GPIO.input(13)==1):
        if (p13.value()==1):
            data |= 0x01
        else:
            data &= 0xFE
        
        data <<= 1
        mask >>= 1
        
    SDA_OUT()
    #time.sleep(0.001)
    if (aknak==1):
        SDA_LO() #NACK for read last read
    else:
        SDA_HI() #ACK for every read
    
    time.sleep(0.001)
    SCL_HI()
    time.sleep(0.001)
    SCL_LO()
    SDA_HI()
    rcvbuf = data
    
def i2c_receive(aknak):
    d = 0
    SDA_OUT()
    SDA_HI()
    SDA_INPUT()
    
    for x in range(0, 8):
        d <<= 1
        
        time.sleep(0.00001)
        SCL_HI()
        #SCL_INPUT()
        
        #while (GPIO.input(15)==0):
        #    time.sleep(0.001)
        time.sleep(0.00001)
        #if (GPIO.input(13)==1):
        if (p13.value()==1):
            d |= 0x01
        else:
            d &= 0xFE
        SCL_LO()
        
    SDA_OUT()
    if (aknak == 0):
        SDA_LO()
    else:
        SDA_HI()    
    SCL_HI()
    time.sleep(0.00001)
    SCL_LO()
    
    SDA_OUT()
    SDA_HI()
    global rcvbuf
    rcvbuf = d

def i2c_send(data):
    mask = 128
    SDA_OUT()
    for x in range(0, 8):
        if (0x80 & data):
            SDA_HI()
        else:
            SDA_LO()
        SCL_HI()
        data <<= 1
        SCL_LO()
    SDA_HI()
    SCL_HI()
    time.sleep(0.00001)
    
    SDA_INPUT() #read ack
    ##if (GPIO.input(13)==1):
    #if (p13.value()==1):
    #    print "NAK"
    #else:
    #    print "ACK"
    SCL_LO()

def main():
    time.sleep(0.005)
    INT_LO()
    RES_LO()
    time.sleep(0.001)
    RES_HI()
    time.sleep(0.005)
    INT_INPUT()
    
    time.sleep(0.005)
    
    i2c_start()
    i2c_send(0xBA)
    i2c_send(0x80) #i2c_send(0x81) 8047
    i2c_send(0x40) #i2c_send(0x4E)
    i2c_send(0x00)
    i2c_stop()

    while True:
        # while (GPIO.input(37)==1): #0 oldugu surece bekle.
            # time.sleep(0.00001)
        i2c_start()
        i2c_send(0xBA)
        i2c_send(0x81) #i2c_send(0x81) 8047
        i2c_send(0x4e) #i2c_send(0x4E)
        i2c_stop()
        while True:
            i2c_start()
            i2c_send(0xBB) ##BB
            global rcvbuf
            rcvbuf = 0
            i2c_receive(1)
            i2c_stop()
            if (rcvbuf & 0x80):
                i2c_start()
                i2c_send(0xBA)
                i2c_send(0x81)
                i2c_send(0x4e)
                i2c_send(0x00)
                i2c_stop()
                i2c_start()
                i2c_send(0xBB)
                myList=[]
                for j in range(0, 6): #39
                    rcvbuf = 0
                    i2c_receive(0)
                    myList.append(rcvbuf)
                rcvbuf = 0
                i2c_receive(1)
                myList.append(rcvbuf)
                # if ((myList[4] * 256 + myList[3]) > 900):
                    #print "X coord" , myList[2] * 256 + myList[1], "Y coord" , myList[4] * 256 + myList[3]
                global xc
                global yc
                if ((myList[2] * 256 + myList[1]) != xc):
                    xc = myList[2] * 256 + myList[1]
                    print ("X coord" , myList[2] * 256 + myList[1], "Y coord" , myList[4] * 256 + myList[3])
                if ((myList[4] * 256 + myList[3]) != yc):
                    yc = myList[4] * 256 + myList[3]
                    print ("X coord" , myList[2] * 256 + myList[1], "Y coord" , myList[4] * 256 + myList[3])
                # print myList
                i2c_stop()
main()