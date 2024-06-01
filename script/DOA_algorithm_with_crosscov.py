import scipy.io.wavfile as wf
import numpy as np
"""
input the separated audio wave file in 2 channels
return a 2-d list indicates the most possible DOA and less possible DOA
"""
def calculate_cross_corr_peaks(channel0,channel1):
    peaks = []
    for i in range(50):
        #take slice of input data
        slice_channel_0 = channel0[int(channel0.shape[0]*i/50):int((channel0.shape[0]*i/50+25))]
        slice_channel_1 = channel1[int(channel1.shape[0]*i/50):int((channel1.shape[0]*i/50+25))]
        cross_corr = np.correlate(slice_channel_0, slice_channel_1, mode='full')
        if np.argmax(cross_corr) >= len(cross_corr)/2:
            peaks.append([np.argmax(cross_corr) - len(cross_corr)/2, "left_right"])
        else:
            peaks.append([len(cross_corr)/2 - np.argmax(cross_corr), "right_left"])
    return peaks

def peak_indices_to_doa(peak_indices, sampling_rate=48000, sensor_distance=0.17):
    time_interval = 1 / sampling_rate
    speed_of_sound = 343.0
    estimated_angles = []
    for peak in peak_indices:
        time_delays = int(peak[0]) * time_interval
        # calculate the angle
        estimated_angle = 90 - np.degrees(np.arccos(speed_of_sound * time_delays / sensor_distance))
        if peak[1] == "left_right":
            estimated_angles.append([estimated_angle, "left_right"])
        else:
            estimated_angles.append([estimated_angle, "right_left"])
    return estimated_angles

def averaging_angles(channel_0_data, channel_1_data):
    try:
        peaks = calculate_cross_corr_peaks(channel_0_data, channel_1_data)
        estimated_angles = peak_indices_to_doa(peaks, sampling_rate=48000, sensor_distance=0.17)
        angles = []
        for angle in estimated_angles:
            if angle[1] == "left_right":
                angles.append((- 1 * angle[0]))
            else:
                angles.append((angle[0]))
        ranges = [[-90,-70],[-70,-50],[-50,-30],[-30,-10],[-10,10],[10,30],[30,50],[50,70],[70,90]]
        DOA = [[],[]]
        for idx in range(len(ranges)):
            freq_range = 0
            for angle in angles:
                if angle > ranges[idx][0] and angle <= ranges[idx][1]:
                    freq_range = freq_range + 1
            if freq_range >= 8:
                DOA[0].append(idx)
            if freq_range >= 5 and freq_range < 7:
                DOA[1].append(idx)

        if DOA[0] != []:
            return DOA
        else:
            return [0]
    except:
        return [0]

if __name__ == "__main__":
    rate, data = wf.read("./loopback_capture_normalized.wav")
    channel_0_data = data[:24000, 0]  # Data from channel 0 (left)
    channel_1_data = data[:24000, 1]  # Data from channel 1 (right)
    print(averaging_angles(channel_0_data, channel_1_data))

"""

    with open('DOA.txt', 'w') as f:
        for line in frequency:
            f.write(f"{str(line)}\n")
import matplotlib.pyplot as plt
# Find peaks in cross-correlation
peaks, _ = find_peaks(cross_corr)
peak = max
print(peaks)
with open('peaks.txt', 'w') as f:
    for line in peaks:
        f.write(f"{str(line)}\n")  

length = channel_0_data[:100].shape[0] / rate
time = np.linspace(0., length, channel_0_data[:100].shape[0])
plt.plot(time, channel_0_data[:100], label="Left channel")
plt.plot(time, channel_1_data[:100], label="Right channel")
plt.plot(time, cross_corr[:100], label="Peak")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
"""
