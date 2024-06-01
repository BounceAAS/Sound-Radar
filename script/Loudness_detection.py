import scipy.io.wavfile as wf
import numpy as np
"""
input the separated audio wave file in 2 channels
return an average loudness of audio(normalized)
"""

def Loudness_dectection(channel_0_data, channel_1_data):
    try:
        mean = np.absolute(channel_0_data).mean()
        #max = np.absolute(channel_0_data).max()
        if mean * 10 // 2 ** 15 >= 5:
            return 3
        elif mean * 10 // 2 ** 15 >= 3:
            return 2
        elif mean * 10 // 2 ** 15 >= 1:
            return 1
        else:
            return 0
    except:
        return 0

if __name__ == "__main__":
    rate, data = wf.read("./loopback_capture_normalized.wav")
    channel_0_data = data[:24000, 0]  # Data from channel 0 (left)
    channel_1_data = data[:24000, 1]  # Data from channel 1 (right)
    print(Loudness_dectection(channel_0_data, channel_1_data))