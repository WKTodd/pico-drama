'''
Christmas diorama controller
by W.K.Todd
V1.0 29/11/2022
'''
import gc
from MP3TFP  import MP3TF
from machine import ADC, Pin, PWM, Timer
from utime   import sleep_ms
from Production import Production
import Scenes 


class Drama(object):
    Optime = 0
    busy_count=2 #busy debounce
    
    def __init__(self):
        self.Swt_off = Pin(22, Pin.IN ,Pin.PULL_UP)
        self.led = Pin(25, Pin.OUT)
        self.Button = Pin(19,Pin.IN, Pin.PULL_UP)
        self.Player_notbusy = Pin(18, Pin.IN, Pin.PULL_UP)
        self.Player_init()
        self.Pot = ADC(28)
        self.Sec_Timer = Timer()
        self.Sec_Timer.init(freq=1, mode=Timer.PERIODIC, callback=self.tick)
        
    
    def tick(self, timer):
        
        self.led.toggle()
        self.Optime +=1
        gc.collect()
        
    def Production_init(self):
        self.Prod = Production(lights = Scenes.lights)
        for Actario in Scenes.acts:
            self.Prod.Create_Act(Actario)
        #self.Prod.Start()
          
        
    def Player_init(self):
        self.Player = MP3TF(txPinNum = 16, rxPinNum = 17)
        sleep_ms(1000)
        self.Player.SetVolume(50)
        sleep_ms(200)
        
    def Player_Start(self):
        self.Player.RandomAll()
        
    def IsPlayerBusy(self):
        running = True
        if self.Player_notbusy.value():
            self.busy_count -=1
            if self.busy_count ==0:
                running = False
        else:
           self.busy_count = 2
        return running
    
    def Run(self):
        self.Production_init()
        while True:
            #main loop
            sleep_ms(200)
            if not self.Button.value():
                self.Player.PlayNext()
            
            if self.Swt_off():
                self.Player.Stop()
                if self.Prod.Running:
                    self.Prod.Start_finale()
            else:
                if not self.IsPlayerBusy():self.Player_Start()
                self.DoVolume()
                if not self.Prod.Running:
                    self.Prod.Start()
                
    def DoVolume(self):
        #min 400 max47000
        Vol = (self.Pot.read_u16()-300)/47000 * 85 #100 reduce max volume to suit 3v supply
        self.Player.SetVolume(Vol)
        


#============================ RUN =================================
#sleep_ms(10000) #wait for mp3 player to initialise
Diorama = Drama()
Diorama.Run()
   
    
    
    
    