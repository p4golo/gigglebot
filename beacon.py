import radio
from microbit import *

def main():
    PREFIX_BEACON  = "00:"
    SECRET_REQUEST = "01:dameSecreto"
    SECRET_MSG     = "02:Tui"
    GROUP_BEACON   = 41
    BEACON_ID1     = 107
    BEACON_ID2     = 51
    BEACON_ID3     = 7
    POWER_BEACON   = 7
    POWER_SECRET   = 0
    PERIOD         = 1000
    BALIZAS = [BEACON_ID1,BEACON_ID2,BEACON_ID3]

    iterator = 0
    radio.on()

    while True:
        display.scroll(str(BALIZAS[iterator]))
        if button_a.is_pressed():
            if iterator < 2:
                iterator +=1
            elif iterator == 2:
                iterator = 0
        if button_b.is_pressed():
            while True:
                radio.config(power =POWER_BEACON,group = GROUP_BEACON)
                radio.send(PREFIX_BEACON+str(BALIZAS[iterator]))
                display.scroll("T")
                sleep(PERIOD)
                received = radio.receive_full()
                if received != None:
                    msg = received[0]
                    msg = str(msg[3:], 'utf8')
                    if msg == SECRET_REQUEST:
                        radio.config(power = POWER_SECRET,group = BALIZAS[iterator])
                        while True:
                            radio.send(SECRET_MSG)
                            sleep(100)
        sleep(PERIOD)

if __name__ == "__main__":
    main()
