#! /usr/bin/python

import paho.mqtt.publish as publish
import math
import struct
import serial
import time

def read_parameter(message, number_answers, coof_trans):

    c_t = 1
    if coof_trans == True:
        c_t = 60

    port = "/dev/ttyUSB0"  
    baudrate = 19200  
  
    ser = serial.Serial(port, baudrate=baudrate)

    print(message)    
    ser.write(message)


    data = ser.read(6 + number_answers * 4) 
    print(data)
    result = []  
  
    if number_answers > 0:
        res = data[4:8]
        result.append(struct.unpack('f', res)[0] * c_t)

    if number_answers > 1:
        res = data[8:12]
        result.append(struct.unpack('f', res)[0] * c_t)

    if number_answers > 2: 
        res = data[12:16]
        result.append(struct.unpack('f', res)[0] * c_t)

    if number_answers > 3:
        res = data[16:20]
        result.append(struct.unpack('f', res)[0] * c_t)
    
    return result

    ser.close()  


def send_data(p):

    for item in p:
        for i in p[item]:
            key = item + "_" + i
            print(key + " " + str(p[item][i]))
            publish.single(key,str(p[item][i]), hostname="127.0.0.1")





msg_active = bytes([64, 3, 8, 0, 0, 0, 187, 72])
msg_reactive = bytes([64, 3, 9, 0, 0, 0, 71, 73])
msg_current = bytes([64, 3, 11, 0, 0, 0, 255, 72])
msg_cos = bytes([64, 3, 12, 0, 0, 0, 139, 73])
msg_temp = bytes([64, 3, 45, 0, 0, 0, 183, 67])
msg_U_f = bytes([64, 3, 10, 0, 0, 0, 3, 73])
msg_energy = bytes([64, 4, 1, 0, 0, 0, 231, 254])


p = {"Active":{"Full":0,
               "A":0,
               "B":0,
               "C":0
              },
     "Reactive":{"Full":0,
                 "A":0,
                 "B":0,
                 "C":0
                },
     "Full":{"Full":0,
             "A":0,
             "B":0,
             "C":0
            },
     "Curr":{"A":0,
             "B":0,
             "C":0
            },
     "Fi":{"A":0,
           "B":0,
           "C":0
          },
     "T":{"Sch":0},
     "U":{"A":0,
          "B":0,
          "C":0
         }, 
     "Energy":{"Active":0,
               "Reactive":0,
               "AReal":0,
               "RReal":0
              }
    }

count = 0
while count < 10:
    active = read_parameter(msg_active, 4, True)
    p["Active"]["Full"] = round(active[0] / 1000, 3)
    p["Active"]["A"] = round(active[1] / 1000, 3)
    p["Active"]["B"] = round(active[2] / 1000, 3)
    p["Active"]["C"] = round(active[3] / 1000, 3)
    
    reactive = read_parameter(msg_reactive, 4, True)
    p["Reactive"]["Full"] = round(reactive[0] / 1000, 3)
    p["Reactive"]["A"] = round(reactive[1] / 1000, 3)
    p["Reactive"]["B"] = round(reactive[2] / 1000, 3)
    p["Reactive"]["C"] = round(reactive[3] / 1000, 3)
    
    p["Full"]["Full"] = round(math.sqrt( p["Active"]["Full"] ** 2 + p["Reactive"]["Full"] ** 2 ), 3)
    p["Full"]["A"] = round(math.sqrt( p["Active"]["A"] ** 2 + p["Reactive"]["A"] ** 2 ), 3)
    p["Full"]["B"] = round(math.sqrt( p["Active"]["B"] ** 2 + p["Reactive"]["B"] ** 2 ), 3)
    p["Full"]["C"] = round(math.sqrt( p["Active"]["C"] ** 2 + p["Reactive"]["C"] ** 2 ), 3)

    curr = read_parameter(msg_current, 3, True)
    p["Curr"]["A"] = round(curr[0],3)
    p["Curr"]["B"] = round(curr[1], 3)
    p["Curr"]["C"] = round(curr[2], 3)
    

    fi = read_parameter(msg_cos, 3, False)
    p["Fi"]["A"] = round(fi[0], 2)
    p["Fi"]["B"] = round(fi[1], 2)
    p["Fi"]["C"] = round(fi[2], 2)

    p["T"]["Sch"] = read_parameter(msg_temp, 1, False)[0]
    u = read_parameter(msg_U_f, 3, False)
    p["U"]["A"] = round(u[0])
    p["U"]["B"] = round(u[1])
    p["U"]["C"] = round(u[2])

    
    
    energy = read_parameter(msg_energy, 4, False)
    p["Energy"]["Active"] = round(energy[0] , 4)
    p["Energy"]["Reactive"] = round(energy[2], 4)
    p["Energy"]["AReal"] = round(energy[0] * 60 , 3)
    p["Energy"]["RReal"] = round(energy[2] * 60 , 3)

    
    send_data(p)
    print("---------------------------------")
    count = count + 1
    time.sleep(5)
