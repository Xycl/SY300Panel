from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ListProperty
from kivy.core.window import Window
from circleknob  import CircleKnob
from xyknob      import XYKnob
from adknob      import ADKnob
from spinnerknob import SpinnerKnob
from switchknob  import SwitchKnob
from toggleknob  import ToggleKnob

#TODO: Add Labels for LFO and OSC

#:import XYKnob xyknob
#:import CircleKnob circleknob
#:import ADKnob adknob
kv = """

<OSC>
    rows: 2
    cols: 5
    #spacing: 1
    padding: 2

    canvas.after:
        Color:
            rgba:[.4, .4 , .4, .7 ]
        Line:
            width:2
            rounded_rectangle: (*self.pos,self.width,self.height, 2)
            
    BoxLayout:
        orientation: 'vertical'
        spacing:2
        Label:
            text: 'OSC ' + root.parent.osc_text
            color: [144/255, 228/255 , 1, 1]      
        MySpinnerKnob:
            id:osc_wave
            addresses: [ 0x01 ]
            text: 'SAW'
            color: [144/255, 228/255 , 1, 1]
            values: ['SIN', 'SAW', 'TRI', 'SQR', 'PWM', 'DETUNE SAW', 'NOISE', 'INPUT']
        BoxLayout:
            
            ToggleKnob:
                text: 'RING'
                color: [144/255, 228/255 , 1, 1]
                size_hint_x: .5
                opacity:  0 if root.parent.is_osc_1 is True else 1     
                disabled: 1 if root.parent.is_osc_1 is True else 0                        
            SpinnerKnob:
                text: 'SYNC'
                color: [144/255, 228/255 , 1, 1]
                values: ['Sync Off', 'Sync On', 'Sync LoFi']
                opacity:   0 if root.parent.is_osc_1 is True else 1
                disabled:  1 if root.parent.is_osc_1 is True else 0                
            
    CircleKnob:
        id: pitch
        text: 'PITCH'
        values: [str(x) for x in range(-24, 25)]
        value: 24
        addresses: [ 0x7 ]
    CircleKnob:
        id: fine
        text: 'FINE'
        values: [str(x) for x in range(-50, 51)]
        value: 50
        addresses: [ 0x8 ]
    CircleKnob:
        id:pulse_width
        text: 'PULSE WIDTH'
        addresses: [ 0x2 ]
        disabled: True if osc_wave.text != 'PWM' else False
    CircleKnob:
        text: 'DETUNE'
        values: [str(x) for x in range(-50, 51)]
        value: 50
        addresses: [ 0x5 ]
        disabled: True if osc_wave.text != 'DETUNE SAW' else False
    CircleKnob:
        text: 'SHARPNESS'
        addresses: [ 0x6 ]
        disabled: True if osc_wave.text != 'NOISE' else False
        
    
    XYKnob:
        text:    'PWM ENV'
        label_x: 'ATTACK'
        label_y: 'DEPTH'
        addresses: [ 0x3, 0x4 ]
        #on_value_x: app.send2midi( root.osc_adr, self.addresses[0], self.value_x )
        #on_value_y: app.send2midi( root.osc_adr, self.addresses[1], self.value_y )
        disabled: True if osc_wave.text != 'PWM' else False
    XYKnob:
        text:    'PITCH ENV'
        label_x: 'ATTACK'
        label_y: 'DEPTH'                                                        
        addresses: [ 0x9, 0xa ]
        #on_value_x: app.send2midi( root.osc_adr, self.addresses[0], self.value_x )
        #on_value_y: app.send2midi( root.osc_adr, self.addresses[1], self.value_y )
    CircleKnob:
        text: 'PBEND DEPTH'
        values: [str(x) for x in range(-24, 25)]
        value: 24
        addresses: [ 0xb ]
        #on_value: app.send2midi( root.osc_adr, self.addresses[0], self.value )
    CircleKnob:
        text: 'PBEND CTL'
        addresses: [ 0xc ]


# ------------------------------ Filter --------------------------------------------
<Filter>
    size_hint_x: 3/5
    spacing: 2
    padding: 5
    rows: 2
    cols: 3
    canvas.after:
        Color:
            rgba:[.4, .4 , .4, .7 ]
        Line:
            width:2
            rounded_rectangle: (*self.pos,self.width,self.height, 2)
    BoxLayout:
        orientation: 'vertical'
        Label:
            text:'FILTER'
            color: [144/255, 228/255 , 1, 1]
        MySpinnerKnob:
            text: 'BYPASS'
            addresses: [ 0x0d ]
            values: ['BYPASS', 'LPF', 'HPF', 'BPF', 'PKG']
            color: [144/255, 228/255 , 1, 1]
        MySpinnerKnob:
            text: '-12 dB'
            addresses: [ 0x0e ]
            color: [144/255, 228/255 , 1, 1]
            values: ['-12 dB', '-24 dB']
        Label:
            text:''
            size_hint_y: .1
        
    
    XYKnob:
        text:       'FILTER'
        label_x:    'CUTOFF'
        label_y:    'RESO'
        labeloffset: 0
        value_x:     0
        value_y:     0
        addresses: [ 0xf, 0x10 ]
    
    XYKnob:
        text:    'ENV'
        label_x: 'ATTACK'
        label_y: 'DEPTH'
        addresses: [ 0x11, 0x12 ]

    ADKnob:
        addresses: [ 0x13 ]
    
    CircleKnob:
        text: 'LEVEL'
        values: [str(x) for x in range(201)]
        value: 100
        addresses: [ 0x14 ]
    CircleKnob: 
        text: 'PAN'
        values: ['L'+str(-x) for x in range(-50, 0)] + ['CTR'] + ['R'+ str(x) for x in range(1, 51)]
        value: 50   
        addresses: [ 0x15 ]

# --------------------------------------LFO ------------------------------
<LFO>
    size_hint_x: .76
    spacing: 2
    padding: 3
 
    rows:2
    cols:4
    canvas.after:
        Color:
            rgba:[.4, .4 , .4, .7 ]
        Line:
            width:2
            rounded_rectangle: (*self.pos,self.width,self.height, 2)
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            padding: 5
            orientation: 'vertical'
            canvas.after:
                Color:
                    rgba:[.4, .4 , .4, .7 ]
                Line:
                    width:1
                    dash_offset: 2
                    dash_length: 5
                    rounded_rectangle: (self.x + 5, self.y + 5,self.width -10, self.height * .85, 2) # *self.size
                    
            Label:    
                text: 'LFO ' + root.parent.osc_text + '/' + str(root.lfo_num + 1)
                color: [144/255, 228/255 , 1, 1]
            MySwitchKnob: #LFO on or off
                addresses: [ 0x17 + 9 * root.lfo_num ]
        MySpinnerKnob:
            size_hint_y: .4
            addresses: [ 0x18 + 9 * root.lfo_num ]
            text: 'SIN'
            color: [144/255, 228/255 , 1, 1]
            values: ['SIN', 'SAW UP', 'SAW DOWN','TRI', 'SQR', 'RANDOM', 'S & H']
         
    CircleKnob:
        id: rate_knob
        text: 'RATE'
        disabled: True if rate_spinner.text != '0-100' else False
                          
    BoxLayout:
        orientation: 'vertical'
        RateComboKnob:
            id: rate_spinner  
            addresses: [ 0x19 + 9 * root.lfo_num ]
            text: '0-100'
            color: [144/255, 228/255 , 1, 1]
            values: ['0-100', 'Whole', 'Dotted Half', 'Triplet Whole', 'Half', 'Dotted Qtr', 'Triplet of Half', 'Qtr', 'Dotted 8th', 'Triplet of Qtr', '8th', 'Dotted 16th','Triplet of 8th', '16th', 'Dotted 32th', 'Triplet of 16th', '32th']
        Label:
            text:''
        MyToggleKnob:    
            id: dyn_depth
            addresses: [ 0x1E + 9 * root.lfo_num ]
            text: 'DYN DEPTH'
            color: [144/255, 228/255 , 1, 1]               
    CircleKnob:
        text: 'FADE TIME'
        addresses: [ 0x1f + 9 * root.lfo_num ]
        disabled: dyn_depth.state == 'normal'       
    CircleKnob:
        text: 'PTCH DPTH'
        addresses: [ 0x1a + 9 * root.lfo_num ]
        #on_value: app.send2midi( root.osc_adr, self.addresses[0], self.value )
    CircleKnob:
        text: 'FLTR DPTH'
        addresses: [ 0x1b + 9 * root.lfo_num  ]
    CircleKnob:
        text: 'AMP DPTH'
        addresses: [ 0x1c + 9 * root.lfo_num ]
    CircleKnob:
        text: 'PWM DPTH'
        addresses: [ 0x1d + 9 * root.lfo_num ]
        disabled: True if root.parent.ids.osc.ids.osc_wave.text != 'PWM' else False
 
 
#------------END LFO DEFINITION                            

# ----------------------------------------The OSC Strip ------------------------
<OSCStrip>: # Derived from BoxLayout
    MySwitchKnob:
        width: 25
        size_hint_x: None   
        id:osc_sw_1
        addresses: [ 0x0 ]
        canvas.before:
            PushMatrix
            Rotate
                angle: 90
                origin: self.center
        canvas.after:
            PopMatrix

    OSC:
        id:osc
    Filter:
    LFO:
        lfo_num: 0
    LFO:               
        lfo_num: 1
#------------------------------ Control Panel using OSCStrip
BoxLayout:
    spacing: 10
    padding: [2,5,5,5]
    orientation:'vertical'
    OSCStrip:
        is_osc_1: True 
        spacing: 5
        osc_text: '1'
        osc_adr: 0x20
    OSCStrip:
        spacing: 5
        osc_text: '2'
        osc_adr: 0x28
    OSCStrip:
        spacing: 5
        osc_text: '3'
        osc_adr: 0x30

"""

class Filter(GridLayout):
    pass


class OSC(GridLayout):
    text = StringProperty('')


class LFO(GridLayout):
    text = StringProperty('')
    lfo_num = NumericProperty( 0 )

class RateComboKnob(SpinnerKnob):
    addresses = ListProperty([])

    # if the spinner is at zero, selecting 0-100, then the knob associated with the spinner is active.
    # There is a single address for the RateComboKnob with values from 0 to 116
    # The logic is in set_knob method of the RateComboKnob class

    def set_knob(self, adr, value):
        if value <= 100:
            self.ids.rate_knob.value = value
            self.text = self.values[0]
        else:
            self.text = self.values[value - 100]

class OSCStrip(BoxLayout):
    is_osc_1 = BooleanProperty(False)
    osc_text = StringProperty('')
    osc_adr  = NumericProperty()

class MySwitchKnob(SwitchKnob):
    addresses = ListProperty([])

class MyToggleKnob(ToggleKnob):
    addresses = ListProperty([])

class MySpinnerKnob(SpinnerKnob):
    addresses = ListProperty([])


class PanelApp(App):
    title = 'SY300 OSC Sound Generation Control Panel'
    Window.size = (1725, 710)
    Window.top = 285  # 0 is the top of the screen
    Window.left = 185
    adr2knob = {}

    def build(self):
        r = Builder.load_string(kv)
        for osc in r.children:    # these children should be the three strips
            for c in osc.walk():
                if hasattr(c, 'addresses'):
                    for a in c.addresses:
                        self.adr2knob[ osc.osc_adr ,  a ] = c

        print('DEBUG: collected knobs for:')
        for k in sorted(self.adr2knob.keys(),key=lambda x: x[0]*100+x[1]):
           print('  ', k , end=' ')
           if hasattr(self.adr2knob[k], 'text'):
               print('  ', k, ' text is ', self.adr2knob[k].text);
           else:
               print('  ', k , '(knob does not have text field)')


        return r

    def send2midi(self, osc, adr, val):
      print( 'message to midi:', osc, adr, val )

PanelApp().run()
