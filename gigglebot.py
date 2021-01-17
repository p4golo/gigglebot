from microbit import sleep,display
import gigglebot
import radio
import distance_sensor

ESTADO = ["escuchando-baliza","buscando-baliza","baliza-encontrada"]
SECRET_REQUEST = "01:dameSecreto"
IDENT_SECRET   = "02:"
GROUP_BEACON   = 41
PERIOD         = 1000

def elegir_baliza(balizas_restantes):
    flag = False
    baliza = "0"
    dBm_baliza = -256
    n_balizas = 0
    while (not flag):
        received = radio.receive_full()
        if received != None:
            msg = received[0]
            msg =str(msg[6:],'utf8')
            dBm = float(received[1])
            if msg != baliza:
                if dBm > dBm_baliza:
                    baliza = msg
                    dBm_baliza = dBm
                display.scroll(msg)
                sleep(100)
                n_balizas += 1
        if n_balizas == balizas_restantes:
            flag = True
        sleep(PERIOD)
    return baliza

def moverse_evitando_obstáculos(ds):
    gigglebot.set_speed(50, 50)
    for i in range(10):
        distance = ds.read_range_single()
        if distance < 100:
            gigglebot.drive(gigglebot.BACKWARD, 500)
            gigglebot.turn(gigglebot.RIGHT,500)
        else:
            gigglebot.drive(gigglebot.FORWARD,500)

def media_dbm(baliza,radio):
    flag = False
    medidas = 6
    n = 0
    sumatorio = 0
    while(not flag):
        received = radio.receive_full()
        if received != None:
            msg = received[0]
            ident = msg[6:]
            dBm = received[1]
            if n > 0:
                sumatorio += float(dBm)
            n += 1
        if n == medidas:
            flag = True
        sleep(100)
    media = sumatorio / (medidas - 1)
    return media
def buscando_baliza(baliza,ds,radio):
    flag = False
    dBm = media_dbm(baliza,radio)
    oldBm = dBm
    while(not flag):
        dBm = media_dbm(baliza,radio)
        if dBm > -60:
            flag = True
            display.scroll("E")
        else :
            if dBm < oldBm:
                gigglebot.turn(gigglebot.RIGHT,500)
                gigglebot.drive(gigglebot.FORWARD,500)
            else:
                moverse_evitando_obstáculos(ds)
        sleep(PERIOD)

def obtener_secreto(baliza,radio):
    flag = False
    solicitar_secreto(radio)
    radio.config(group=int(baliza),power = 7)
    while (not flag):
        received = radio.receive_full()
        if received != None :
            msg = received[0]
            ident_secret = str(msg[3:6],'utf8')
            if ident_secret == IDENT_SECRET:
                secreto = msg[6:]
                flag = True
        sleep(100)
    return secreto

def solicitar_secreto(radio):
    radio.config(group=GROUP_BEACON,power = 7)
    for i in range(5):
        radio.send(SECRET_REQUEST)
        sleep(100)

def main():
    balizas_restantes = 3
    iterator = 0
    radio.on()
    flag = False
    ds = distance_sensor.DistanceSensor()
    while(not flag):
        radio.config(group=GROUP_BEACON, queue = 1)
        if ESTADO[iterator] == "escuchando-baliza":
            baliza = elegir_baliza(balizas_restantes)
            display.scroll(baliza)
            iterator += 1
        if ESTADO[iterator] == "buscando-baliza":
            buscando_baliza(baliza,ds,radio)
            iterator +=1
        if ESTADO[iterator] == "baliza-encontrada":
            secreto = obtener_secreto(baliza,radio)
            iterator = 0
            balizas_restantes -= 1
            display.scroll(secreto)
        if balizas_restantes == 0:
            gigglebot.stop()
            flag = True
            display.scroll("FIN")
        sleep(PERIOD)

if __name__ == "__main__":
    main()

