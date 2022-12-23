'''Production objects for lamp fading etc.'''
from machine import Pin, PWM, Timer
from utime   import sleep_ms

class Lamp(object):
    '''Lamp object - controls PWM output of pin to allow fades and delays'''
    Level = 0 #target level 0= off 100=full on
    Fadetime = None
    _delay = 0 # xx milliseconds 
    _currentlevel = 0 #level 0=off 65535 = full    
    _pwmlevel = 0 # target level 0=off 65535 = full
    _fadeincrement =0
    _scenefadeoverride = False
    
    def __init__(self, production = None, name = "", GP_number=0):       
        self._production = production 
        self.Pin = Pin(GP_number)
        self.Pwm = PWM(self.Pin)
        self.Pwm.freq(500)
        self.Pwm.duty_u16(0)
        
    def SetLevel(self, level =0):
        self.Level = level
        self._pwmlevel = int(level* 655.35)
        self.calc_inc()
        
    def SetFadetime(self, time =0): #time in seconds
        self.Fadetime = time
        self.calc_inc()
        
    def SetDelay(self, delay):
        self._delay = delay * self._production.FaderFreq
        
    def SetSceneOverride(self, SOR = False):
        self._scenefadeoverride = SOR
        if SOR:
            self._fadeincrement = (self._pwmlevel- self._currentlevel) \
                                   /(self._scene.Fadetime() * \
                                     self._production.FaderFreq)
        else:
            self.calc_inc()
        
    def calc_inc(self):
        if self.Fadetime:
            self._fadeincrement = (self._pwmlevel - self._currentlevel)/ \
                                  (self.Fadetime * \
                                    self._production.FaderFreq)
        else:
            self._fadeincrement = self._pwmlevel
            
    def Fade(self):
        #called at intervals by Production
        if self._delay <=0:
            if self._fadeincrement > 0:
                if self._currentlevel <= self._pwmlevel:
                    self._currentlevel = min( self._currentlevel + self._fadeincrement, 65535)
                    self.Pwm.duty_u16(int(self._currentlevel))
            else:
                if self._currentlevel > self._pwmlevel:
                    self._currentlevel= max(self._currentlevel + self._fadeincrement ,0)
                    self.Pwm.duty_u16(int(self._currentlevel))
        else:
            self._delay -=1
        
class Scene(object):
    '''scene object for production class'''
    
    Lampset = [] #list of lamp settings (lamp object, targetlevel , fadetime, delay),

    Duration =0
    _production = None
    _timer = None
    _group = None
    
    def __init__(self, production=None, lampsetlist = [], duration =0, ):
        self._production = production
        self.Lampset = lampsetlist
        self.Duration = duration
        self._timer = Timer()

              
    def Open(self):
        #set target levels for each lamp
        for LS in self.Lampset:
            LS[0].SetLevel(LS[1])
            LS[0].SetFadetime(LS[2])
            if len(LS)>3:
                LS[0].SetDelay(LS[3])
            else:
                LS[0].SetDelay(0)
                
        self._timer.init(period = self.Duration*1000, mode=Timer.ONE_SHOT, callback=self._done)
            
    def Close(self):        
        self._timer.deinit()
    
    def _done(self,timer):
        print("scene._done", self._group)
        if self._group:
            self._group._sceneover(self)
        else:
            self._production._sceneover(self)
        
class Act(object):
    '''Act object contains a group of scenes that can repeat or single play'''
    CurrentScene = 0
    Cycle = False
    _scenes = []
    def __init__(self, production = None, name = "", scenelist=[], cycle = False):
        self.Name = name
        self.Cycle = cycle
        self._scenes = scenelist
        self.Prod = production
        for S in self._scenes:
            S._group = self
    
    def Open(self):
        self.CurrentScene=0  
        self._scenes[self.CurrentScene].Open()        
        
    def _sceneover(self, scene):
        self.CurrentScene +=1
        if self.CurrentScene >= len(self._scenes):
            if self.Cycle:
                self.CurrentScene=0  
                self._scenes[self.CurrentScene].Open()
                print("open scene:",self.CurrentScene)
            else:
                self.Prod._actover(self)
        else:
            self._scenes[self.CurrentScene].Open()
            print("open scene:",self.CurrentScene)            
                
    def Terminate(self):
        for S in self._scenes:
            S.Close()
        self.Prod._actover(self)
                 
class Production(object):
    '''Production object encapsulates acts ,scenes & lamps etc'''
    CurrentScene =0
    CurrentAct =0
    _acts = []
    _scenes = []
    _fader = None
    FaderFreq = 50
    Lamps = {} #dict {"name":Lamp object,}
    Running = False
    def __init__(self, lights = {}):# lights = dict of all lights {"name":GPIO_number,}
        
        self._fader = Timer()
        self.init_lamps(lights)
        
    def Start(self):
        self._fader.init(period = int(1000/self.FaderFreq),
                         mode=Timer.PERIODIC,
                         callback=self._fadelamps)
        self.CurrentScene =0
        self.CurrentAct = 0
        self._acts[self.CurrentAct].Open()
        self.Running = True
    
    def Stop(self):
        #all lights off
        for lamp in self.Lamps:
            lamp.SetLevel(0)
            lamp.SetFadetime = None
        sleep_ms(100) 
        self._fader.deinit()
        
    def Start_finale(self):
        for N in range(0,len(self._acts)-1):
            self._acts[N].Terminate()          
        
    def init_lamps(self, lights):
        for name, gpn in lights.items():
            self.Lamps[name] = Lamp(self,name,gpn)
                
    def Create_Scene(self, scenario):
        '''scenario = [
                        [
                        ("lampname",level, fadetime, delay), #lamp0 of n...
                        ] #senario[0]
                        , scene_duration #scenario[1]
                     ] 
        '''
        new_lampset=[]
        
        for lamp in scenario[0]:
            new_lampset.append((self.Lamps[lamp[0]],lamp[1], lamp[2], lamp[3]))
            #print(new_lampset)
        new_scene = Scene(self, new_lampset, scenario[1])
        self._scenes.append(new_scene)
        return new_scene
    
    def Create_Act(self, actario):
        '''act1 = {"act1":([startscene,...],cycle =False)}'''
        for key, value in actario.items():
            SL=[]
            for scenario in value[0]:
                SL.append(self.Create_Scene(scenario))
            
            new_act = Act(production = self, name=key, scenelist=SL ,cycle=value[1])
            self._acts.append(new_act)

    def _fadelamps(self, timer):
        #called every xxmS by timer
        for name, lamp in self.Lamps.items():
            lamp.Fade()
            
    def _actover(self, act):
        self.CurrentAct +=1
        if self.CurrentAct < len(self._acts):
            self._acts[self.CurrentAct].Open()
            print("open act:",self.CurrentAct)
        else:
            self.Running = False

    def _sceneover(self, scene):        
        self.CurrentScene +=1
        if self.CurrentScene >= len(self._scenes):
                self.CurrentScene=0
        #print(scene, self.CurrentScene)    
        self._scenes[self.CurrentScene].Open()            
            