from time import time
import RPi.GPIO as GPIO
import time
import  math

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
    
ledResistencia = 7
led40graus = 8
led30min = 33
led60min = 35
led90min = 37
led120min = 29
led180graus = 11
led220graus = 12
led250graus = 13
ledPower = 22
ledDesabilitado = 36
ledExaustao = 26

botaoPower = 16
botaoTemperatura = 18
botaoDesabilita = 32
botaoTemporarizador = 31
botaoConfirmar = 15
botaoExaustor = 24

contador = 0
contadorInteracao = 0 

botaoControle = False
contadortempo = 0
temperaturaAjustada = False
confirmarTempo = False
confirmaDesligado = False
confirmaResfriamento = False
confirmaDesabilita = False

tempo1 = 40
tempo2 = 60
tempo3 = 80
tempo4 = 100
tempoExaustao = 5

'''Setando leds
    GPIO 11 = temp 180
    GPIO 12 = temp 220
    GPIO 13 = temp 250
    GPIO 22 = LIGA/DESLIGA
    GPIO 36 = Desabilitado
    GPIO 33 = led tempo 30 min
    GPIO 35 = led tempo 60 min
    GPIO 37 = led tempo 90 min
    GPIO 29 = led tempo 120 min 
    GPIO 07 = Resistencia
    GPIO 08 = TEMPERATURA ACIMA 40
    '''
GPIO.setup(led40graus, GPIO.OUT)
GPIO.setup(ledResistencia, GPIO.OUT)
GPIO.setup(led30min, GPIO.OUT)
GPIO.setup(led60min, GPIO.OUT)
GPIO.setup(led90min, GPIO.OUT)
GPIO.setup(led120min, GPIO.OUT)
GPIO.setup(led180graus, GPIO.OUT)
GPIO.setup(led220graus, GPIO.OUT)
GPIO.setup(led250graus, GPIO.OUT)
GPIO.setup(ledPower, GPIO.OUT)
GPIO.setup(ledDesabilitado, GPIO.OUT)
GPIO.setup(ledExaustao, GPIO.OUT)

''' Botoes
    GPIO 18 = Seleciona temperatura
    GPIO 16 = ON/OFF
    GPIO 32 = desabilita
    GPIO 31 = controle tempo
    GPIO 15 = Confirma tempo 
    '''
GPIO.setup(botaoTemperatura, GPIO.IN)
GPIO.setup(botaoPower, GPIO.IN)
GPIO.setup(botaoDesabilita, GPIO.IN)
GPIO.setup(botaoTemporarizador, GPIO.IN)
GPIO.setup(botaoConfirmar, GPIO.IN)
GPIO.setup(botaoExaustor, GPIO.IN)

''' Led iniciando em baixa
'''
GPIO.output(led40graus, False)
GPIO.output(ledResistencia, False)
GPIO.output(led30min, False)
GPIO.output(led60min, False)
GPIO.output(led90min, False)
GPIO.output(led120min, False)
GPIO.output(led180graus, False)
GPIO.output(led220graus, False)
GPIO.output(led250graus, False)
GPIO.output(ledPower, False)
GPIO.output(ledDesabilitado, False)
GPIO.output(ledExaustao, False)

while(1):
    if GPIO.input(botaoPower) == True:
        time.sleep(0.5)
        if botaoControle is True:
            botaoControle = False
            contador = 0           
            GPIO.output(led180graus, False)
            GPIO.output(led220graus, False)
            GPIO.output(led250graus, False)
            GPIO.output(ledDesabilitado, False)
            GPIO.output(ledPower, False)
            GPIO.output(led30min, False)
            GPIO.output(led60min, False)
            GPIO.output(led90min, False)
        else:
            botaoControle = True
            GPIO.output(ledDesabilitado, True)
            GPIO.output(ledPower, True)
    if botaoControle == True:
        if contador != 0:
                GPIO.output(ledDesabilitado, False)
        if GPIO.input(botaoDesabilita) == True:
            GPIO.output(led180graus, False)
            GPIO.output(led220graus, False)
            GPIO.output(led250graus, False)
            GPIO.output(led30min, False)
            GPIO.output(led60min, False)
            GPIO.output(led90min, False)
            GPIO.output(ledDesabilitado, True)
            contador = 0
            contadortempo = 0            
        if GPIO.input(botaoTemperatura) == True:
            contador = contador +1
            if (contador > 0 and contador < 4):
                temperaturaAjustada = True
            else:
                temperaturaAjustada = False
            time.sleep(0.5)
            if contador == 1:
                GPIO.output(led180graus, True)
                print("Forno ligado a 180")
            elif contador == 2:
                GPIO.output(led180graus, False)
                GPIO.output(led220graus, True)
                print("Forno ligado a 220")
            elif contador == 3:
                GPIO.output(led220graus, False)
                GPIO.output(led250graus, True)
                print("Forno ligado a 250")
            elif contador == 4:
                GPIO.output(led180graus, False)
                GPIO.output(led220graus, False)
                GPIO.output(led250graus, False)
                print("Selecione uma temperatura")
                contador = 0
        if GPIO.input(botaoTemporarizador) == True and temperaturaAjustada == True:
            if (contador > 0):
                contadortempo = contadortempo +1
                time.sleep(0.5)                
                if contadortempo == 1:
                    GPIO.output(led30min, True)
                    print("30 min")   
                elif contadortempo == 2:
                    GPIO.output(led30min, False)
                    GPIO.output(led60min, True)
                    print("60 min")
                elif contadortempo == 3:
                    GPIO.output(led60min, False)
                    GPIO.output(led90min, True)
                    print("90 min")
                elif contadortempo == 4:
                    GPIO.output(led90min, False)
                    GPIO.output(led120min, True)
                    print("120 min")
                elif contadortempo == 5:
                    GPIO.output(led30min, False)
                    GPIO.output(led60min, False)
                    GPIO.output(led90min, False)
                    GPIO.output(led120min, False)          
                    print("Selecione o tempo desejado")
                    contadortempo = 0
        if GPIO.input(botaoConfirmar) == True:
            time.sleep(0.5)
            if contadortempo == 1:
                if contador == 1:
                    t = time.time()
                    while (time.time() - t < tempo1):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                                                     
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 29.9 and (time.time() - t) < 30):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led180graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 39.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break        
                                                                                                                    
            if contadortempo == 2:              
                if contador == 1:
                    t = time.time()
                    while (time.time() - t < tempo2):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                                                     
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 49.9 and (time.time() - t) < 50):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led180graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 59.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)    
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break                                
            if contadortempo == 3:
                if contador == 1:
                    t = time.time()
                    while (time.time() - t < tempo3):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                          
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 69.9 and (time.time() - t) < 70):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led180graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 79.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break               
            if contadortempo == 4:
                if contador == 1:
                    t = time.time()
                    while (time.time() - t < tempo4):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                          
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 89.9 and (time.time() - t) < 90):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led120min, False)
                            GPIO.output(led180graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 99.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break               
            if contadortempo == 1:
                if contador == 2:
                    t = time.time()
                    while (time.time() - t < tempo1):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                                                     
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 29.9 and (time.time() - t) < 30):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led220graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 39.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break                                                            
            if contadortempo == 2:              
                if contador == 2:
                    t = time.time()
                    while (time.time() - t < tempo2):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                                                     
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 49.9 and (time.time() - t) < 50):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led220graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 59.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break                         
            if contadortempo == 3:
                if contador == 2:
                    t = time.time()
                    while (time.time() - t < tempo3):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                          
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 69.9 and (time.time() - t) < 70):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led220graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 79.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break            
            if contadortempo == 4:
                if contador == 2:
                    t = time.time()
                    while (time.time() - t < tempo4):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                          
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 89.9 and (time.time() - t) < 90):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led120min, False)
                            GPIO.output(led220graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 99.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break               
            if contadortempo == 1:
                if contador == 3:
                    t = time.time()
                    while (time.time() - t < tempo1):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                                                     
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 29.9 and (time.time() - t) < 30):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led250graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 39.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break                                                               
            if contadortempo == 2:              
                if contador == 3:
                    t = time.time()
                    while (time.time() - t < tempo2):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                                                     
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 49.9 and (time.time() - t) < 50):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led250graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 59.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break                          
            if contadortempo == 3:
                if contador == 3:
                    t = time.time()
                    while (time.time() - t < tempo3):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                          
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 69.9 and (time.time() - t) < 70):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led250graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 79.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break            
            if contadortempo == 4:
                if contador == 3:
                    t = time.time()
                    while (time.time() - t < tempo4):
                        if GPIO.input(botaoDesabilita) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledDesabilitado, True)
                            contador = 0
                            contadortempo = 0                          
                        if ((time.time() - t) > 0 and (time.time() - t) < 1):
                            GPIO.output(ledResistencia, True)
                        if ((time.time() - t) > 89.9 and (time.time() - t) < 90):
                            GPIO.output(ledResistencia, False)
                            GPIO.output(led120min, False)
                            GPIO.output(led250graus, False)
                        if ((time.time() - t) > 10):     
                            if math.fmod((int)(time.time() - t),  2) == 0:
                                GPIO.output(led40graus, True) 
                            else:
                                GPIO.output(led40graus, False)                      
                        if ((time.time() - t) > 99.8):
                            contador = 0
                            contadortempo = 0
                            GPIO.output(led40graus, False)
                        if GPIO.input(botaoExaustor) == True:
                            GPIO.output(led180graus, False)
                            GPIO.output(led220graus, False)
                            GPIO.output(led250graus, False)
                            GPIO.output(led30min, False)
                            GPIO.output(led60min, False)
                            GPIO.output(led90min, False)
                            GPIO.output(led120min, False)
                            GPIO.output(ledResistencia, False)
                            GPIO.output(ledExaustao, True)
                            contador = 0
                            contadortempo = 0 
                            t = time.time()
                            while (time.time() - t < tempoExaustao):
                                if ((time.time() - t) > 0):     
                                    if math.fmod((int)(time.time() - t),  2) == 0:
                                        GPIO.output(led40graus, True) 
                                    else:
                                        GPIO.output(led40graus, False)                      
                                if ((time.time() - t) > 4.8):
                                    contador = 0
                                    contadortempo = 0
                                    GPIO.output(led40graus, False)
                            GPIO.output(ledExaustao, False)
                            GPIO.output(ledDesabilitado, True)
                            break                                                        
    else:
        confirmaDesligado = True
