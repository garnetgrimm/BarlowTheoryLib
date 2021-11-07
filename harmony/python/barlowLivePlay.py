import pyaudio
import numpy as np
import random
import barlow

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 6.0   # in seconds, may be float

ratios = barlow.calcAllIntervals(0.1, True)

harms = []
sum = 0
for harm in list(ratios.keys()):
    harm = abs(harm)
    if(harm >= 1.0): harm = 0.0
    sum += harm
    harms.append(harm)

for i in range(len(harms)):
    harms[i] = (harms[i]/sum) * 100

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively)
minF = 100.00
bf = 250.0
f = 250.0
maxF = 450.00

freqList = []
for n in range(3):
    newPhrase = []
    #f = bf
    for i in range(16):
        newPhrase.append(f)
        ratio = random.choices(list(ratios.values()), weights=harms, k=1)[0]
        height = ((f-minF)/(maxF-minF))
        doInc =  random.uniform(0.0, 1.0) > height
        if(doInc): freqRatio = ratio[1] / ratio[0]
        else: freqRatio = ratio[0] / ratio[1]
        f = f*freqRatio
    newPhrase *= 1
    freqList += newPhrase
#f = bf
newPhrase = []
for i in range(0):
    newPhrase.append(f)
    ratio = random.choices(list(ratios.values()), weights=harms, k=1)[0]
    height = ((f-minF)/(maxF-minF))
    doInc =  random.uniform(0.0, 1.0) > height
    if(doInc): freqRatio = ratio[1] / ratio[0]
    else: freqRatio = ratio[0] / ratio[1]
    f = f*freqRatio
    freqList += [f]
    print(f)

for i in range(0, len(freqList)-4, 4):
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*freqList[i+1]/fs)).astype(np.float32)
    samples += (np.sin(2*np.pi*np.arange(fs*duration)*freqList[i+2]/fs)).astype(np.float32)
    samples += (np.sin(2*np.pi*np.arange(fs*duration)*freqList[i+3]/fs)).astype(np.float32)
    samples += (np.sin(2*np.pi*np.arange(fs*duration)*freqList[i+4]/fs)).astype(np.float32)
    volume = 0.25*(np.sin(0.5*np.pi*np.arange(fs*duration)/fs)).astype(np.float32)
    np.multiply(samples, volume)
    stream.write(volume*samples)

stream.stop_stream()
stream.close()

p.terminate()