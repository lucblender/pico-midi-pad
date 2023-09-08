import machine
from machine import Pin
import utime
import time
import ustruct

COL_NUMBER = 6
ROW_NUMBER = 8

last_key_update = time.time()

col_list_pin=[16,17,18,19,20,21]
row_list_pin=[8,9,10,11,12,13,15,14]
col_list = [0,0,0,0,0,0]
row_list = [0,0,0,0,0,0,0,0]

uart = machine.UART(0,baudrate=31250,tx=Pin(0),rx=Pin(1))
led_uart = Pin(28, Pin.OUT)
led_a = Pin("LED", Pin.OUT)
led_b = Pin(22, Pin.OUT)

enc_midi_0 = Pin(2, Pin.IN, Pin.PULL_UP)
enc_midi_1 = Pin(3, Pin.IN, Pin.PULL_UP)
enc_midi_2 = Pin(4, Pin.IN, Pin.PULL_UP)
enc_midi_3 = Pin(5, Pin.IN, Pin.PULL_UP)

led_a.value(1)
led_b.value(1)

global_midi_channel = 1


class MidiNote:
    def __init__(self, note, velocity, midi_channel = -1):
        self.note = note
        self.velocity = velocity
        self.midi_channel = midi_channel
        

for x in range(0,ROW_NUMBER):
    row_list[x]=Pin(row_list_pin[x], Pin.OUT)
    row_list[x].value(1)


for x in range(0,COL_NUMBER):
    col_list[x] = Pin(col_list_pin[x], Pin.IN, Pin.PULL_UP)
    
SW_CONFIGURATION = 0

SW0_x_index  = 2
SW0_y_index  = 5
SW1_x_index  = 3
SW1_y_index  = 5

key_map= [
    ["A1","C1","E1","H1","G1","K0"],
    ["A0","C0","E0","H0","G0","K1"],
    ["A3","C3","E3","H3","G3","SW0"],
    ["A2","C2","E2","H2","G2","SW1"],
    ["B0","D0","F0","I0","J0","unused"],
    ["B1","D1","F1","I1","J1","unused"],
    ["B2","D2","F2","I2","J2","unused"],
    ["B3","D3","F3","I3","J3","unused"]
]

note_map=[
            # first patch for volca drum
            [[MidiNote(49,64,1) ,MidiNote(49,64,3),MidiNote(49,127,7),MidiNote(49,64,6),MidiNote(49,64,5),MidiNote(49,127,7)],
            [MidiNote(49,127,1) ,MidiNote(49,127,3),MidiNote(49,127,7),MidiNote(49,127,6),MidiNote(49,127,5),MidiNote(49,127,7)],
            [MidiNote(49,16,1) ,MidiNote(49,16,3),MidiNote(49,127,7),MidiNote(49,16,6),MidiNote(49,16,5),MidiNote(49,127,7)],
            [MidiNote(49,32,1) ,MidiNote(49,32,3),MidiNote(49,127,7),MidiNote(49,32,6),MidiNote(49,32,5),MidiNote(49,127,7)],
            [MidiNote(49,127,2) ,MidiNote(49,127,4),MidiNote(49,127,7),MidiNote(49,127,7),MidiNote(49,127,7),MidiNote(49,127,7)],
            [MidiNote(49,64,2) ,MidiNote(49,64,4),MidiNote(49,127,7),MidiNote(49,127,7),MidiNote(49,127,7),MidiNote(49,127,7)],
            [MidiNote(49,32,2) ,MidiNote(49,32,4),MidiNote(49,127,7),MidiNote(49,127,7),MidiNote(49,127,7),MidiNote(49,127,7)],
            [MidiNote(49,16,2) ,MidiNote(49,16,4),MidiNote(49,127,7),MidiNote(49,127,7),MidiNote(49,127,7),MidiNote(49,127,7)]],
            
            #second patch for drum brut note from 36 to 45 for normal and from 48 to 57 (54 doesn't exist, cowbell only has one mode)
            [[MidiNote(36,127,-1) ,MidiNote(38,127,-1),MidiNote(49,0,-1),MidiNote(39,127,-1),MidiNote(45,127,-1),MidiNote(42,127,-1)],
            [MidiNote(48,127,-1) ,MidiNote(50,127,-1),MidiNote(49,0,-1),MidiNote(51,127,-1),MidiNote(57,127,-1),MidiNote(42,  1,-1)],
            [MidiNote(36,  1,-1) ,MidiNote(38,  1,-1),MidiNote(49,0,-1),MidiNote(39,  1,-1),MidiNote(45,  1,-1),MidiNote(49,127,-1)],
            [MidiNote(48,  1,-1) ,MidiNote(50,  1,-1),MidiNote(49,0,-1),MidiNote(51,  1,-1),MidiNote(57,  1,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(53,127,-1),MidiNote(55,127,-1),MidiNote(56,127,-1),MidiNote(52,127,-1),MidiNote(49,127,-1)],
            [MidiNote(37,127,-1) ,MidiNote(41,127,-1),MidiNote(43,127,-1),MidiNote(44,127,-1),MidiNote(40,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,  1,-1) ,MidiNote(53,  1,-1),MidiNote(55,  1,-1),MidiNote(56,  1,-1),MidiNote(52,  1,-1),MidiNote(49,127,-1)],
            [MidiNote(37,  1,-1) ,MidiNote(41,  1,-1),MidiNote(43,  1,-1),MidiNote(44,  1,-1),MidiNote(40,  1,-1),MidiNote(49,127,-1)]],
            
            [[MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)]],
            
            [[MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)],
            [MidiNote(49,127,-1) ,MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1),MidiNote(49,127,-1)]]
            
        ]


key_state = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
key_state_old = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

def send_note_midi_on(midiNote):
    global uart, led_uart, global_midi_channel
    if midiNote.midi_channel == -1:
        channel = global_midi_channel
    else:
        channel = midiNote.midi_channel
    print("__send_note_midi_on", midiNote.note, midiNote.midi_channel,midiNote.velocity)
    uart.write(ustruct.pack("bbb",0x90+(channel-1),midiNote.note,midiNote.velocity))
    led_uart.value(1)

def send_note_midi_off(midiNote):
    global uart, led_uart, global_midi_channel
    if midiNote.midi_channel == -1:
        channel = global_midi_channel
    else:
        channel = midiNote.midi_channel
    print("__send_note_midi_off", midiNote.note, midiNote.midi_channel)
    uart.write(ustruct.pack("bbb",0x80+(channel-1),midiNote.note,0))
    led_uart.value(0)


def KeypadRead(cols,rows):
    global key_state
    global key_state_old
    global last_key_update
    global note_map
    global SW0_x_index, SW0_y_index, SW1_x_index, SW1_y_index, SW_CONFIGURATION
    
    key_state = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
    for r in range(0, ROW_NUMBER):
        #put pin as output
        Pin(row_list_pin[r], Pin.OUT)
        rows[r].value(0)
        for c in range(0,COL_NUMBER):
            if cols[c].value() == 0:       
                    key_state[r][c] = 1

            if(key_state[r][c] != key_state_old[r][c]):
                last_key_update = time.time()
                key=key_map[r][c]
                if key_state[r][c] == 0 and key not in ["SW0", "SW1"]:
                    print("released", key)
                    send_note_midi_off(note_map[SW_CONFIGURATION][r][c])
                elif key_state[r][c] == 1  and key not in ["SW0", "SW1"]:
                    print("pressed", key)
                    send_note_midi_on(note_map[SW_CONFIGURATION][r][c])  
        #put pin as input to have high z
        Pin(row_list_pin[r], Pin.IN)
        
    SW_CONFIGURATION = key_state[SW0_x_index][SW0_y_index]+2*key_state[SW1_x_index][SW1_y_index]

    for x in range(0, ROW_NUMBER):
        for y in range(0, COL_NUMBER):
            key_state_old[x][y] = key_state[x][y]

def midi_channel_read():
    global enc_midi_0, enc_midi_1,enc_midi_2, enc_midi_3
    global global_midi_channel
    global_midi_channel = ((1- enc_midi_0.value())+2*(1- enc_midi_1.value())+4*(1- enc_midi_2.value())+8*(1- enc_midi_3.value()) + 1)
    #print(global_midi_channel)      

try:    
    time.sleep(0.5)
    while True:      
        key=KeypadRead(col_list, row_list)
        midi_channel_read()
     
except Exception as e:
    print(e)
