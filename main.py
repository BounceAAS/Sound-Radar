import scipy.io.wavfile as wf
import sys
from script.SoundCapture import AudioLoopbackCapture
from script.SoundNormalization import SoundNormalization
from script.DOA_algorithm_with_crosscov import averaging_angles
from script.Loudness_detection import Loudness_dectection
from script.Sound_classification import Sound_classification

def main(classification, model_path = './model/net.onnx'):
    DURATION = 0.5
    CHUNK_SIZE = 512

    # give the path relative to main.py
    filepath = "./temp/loopback_capture.wav"

    AudioLoopbackCapture(DURATION, CHUNK_SIZE, filepath)
    SoundNormalization(input_file_path="./temp/loopback_capture.wav",
                       output_file_path="./temp/loopback_capture_normalized.wav", output_format="wav")

    rate, data = wf.read("./temp/loopback_capture_normalized.wav")
    channel_0_data = data[:24000, 0]  # Data from channel 0 (left)
    channel_1_data = data[:24000, 1]  # Data from channel 1 (right)

    DOA = averaging_angles(channel_0_data, channel_1_data)
    Loudness = Loudness_dectection(channel_0_data, channel_1_data)

    if classification == "o":
        Sound_class = Sound_classification("./temp/loopback_capture_normalized.wav", model_path)
        return [DOA, Loudness, Sound_class]
    else:
        return [DOA, Loudness, "Null"]



if __name__ == "__main__":
    DURATION = 0.5
    CHUNK_SIZE = 512

    # give the path relative to main.py
    filepath = "./temp/loopback_capture.wav"
    default_model_path = './model/net.onnx'

    # can take two parameters
    if len(sys.argv) == 3:
        classification = str(sys.argv[1])
        model_path = './model/' + str(sys.argv[2]) + '.onnx'
    elif len(sys.argv) == 1:
        classification = "f"
        model_path = default_model_path
    else:
        print("invalid arguments")

    AudioLoopbackCapture(DURATION, CHUNK_SIZE, filepath)
    SoundNormalization(input_file_path="./temp/loopback_capture.wav",
                       output_file_path="./temp/loopback_capture_normalized.wav", output_format="wav")

    rate, data = wf.read("./temp/loopback_capture_normalized.wav")
    channel_0_data = data[:24000, 0]  # Data from channel 0 (left)
    channel_1_data = data[:24000, 1]  # Data from channel 1 (right)

    DOA = averaging_angles(channel_0_data, channel_1_data)
    Loudness = Loudness_dectection(channel_0_data, channel_1_data)

    if classification == "o":
        Sound_class = Sound_classification("./temp/loopback_capture_normalized.wav", model_path)
        with open('./temp/outputs.txt', 'w') as f:
            for item in [DOA[0], DOA[1], Loudness, Sound_class]:
                f.write(f"{str(item)}\n")
        print([DOA, Loudness, Sound_class])

    else:
        with open('./temp/outputs.txt', 'w') as f:
            for item in [DOA[0], DOA[1], Loudness, "Null"]:
                f.write(f"{str(item)}\n")
        print([DOA, Loudness, "Null"])


