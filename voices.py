from __future__ import division
from matplotlib import pylab as plt
import numpy as np
import scipy.io.wavfile
from scipy.signal import kaiser
import os, re

correct_count = 0

def analyze(filename):
  global correct_count

  print('analyzing ' + filename + ' ...')
  try:
    sampling_rate, signal = scipy.io.wavfile.read(filename)
  except:
    print("unable to analyze " + filename)
    print("")
  else:
    samples_count = len(signal)
    duration = float(samples_count) / sampling_rate
    if not isinstance(signal[0], np.int16):
      signal = [s[0] for s in signal]
    signal = signal * kaiser(samples_count, 100)

    frequency = np.fft.rfft(signal)
    frequency = abs(frequency)
    peak_start = 50 * duration
    peak = np.argmax(frequency[peak_start:])
    fundamental = (peak_start + peak) / duration

    if 85 < fundamental < 165:
      verdict = 'M'
    elif 180 < fundamental < 255:
      verdict = 'F'
    else:
      verdict = 'U'

    correct = re.search('([KM])\.wav', filename).group(1)
    if correct == 'K':
      correct = 'F'

    if correct == verdict:
      correct_count += 1

    print("fundamendal frequency: " + "%.5f" % fundamental)
    print("verdict: " + verdict)
    print("")

    #print(sampling_rate, duration, len(frequency[::duration]))

    #plt.plot(frequency[0:3000])
    #plt.show()

filenames = os.listdir('wav')
for filename in filenames:
  analyze('wav/' + filename)

accuracy = float(correct_count) / len(filenames)
print("accuracy: %.2f%%" % (accuracy * 100))

#analyze('wav/002_M.wav')
