from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
t = TonalBuzzer(22) # change to whatever pin the buzzer is connected

v1 = ["G4", "G4", "G4", "D4", "E4", "E4", "D4"]
v2 = ["B4", "B4", "A4", "A4", "G4"]
v3 = ["D4", "G4", "G4", "G4", "D4", "E4", "E4", "D4"]

song = [v1,v2]

while(True):
  for verse in song:
      for note in verse:
          t.play(note)
          sleep(0.4)
          t.stop()
          sleep(0.1)
      sleep(0.2)