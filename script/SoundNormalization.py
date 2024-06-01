from pydub import AudioSegment, effects

def SoundNormalization(input_file_path = "./loopback_capture.wav", output_file_path = "./loopback_capture_normalized.wav", output_format = "wav"):
    """unify the channel number and sample rate of audio"""
    rawsound = AudioSegment.from_file(input_file_path)
    sound = rawsound.set_channels(2)
    sound = sound.set_frame_rate(48000)
    """normaolize the loudness of audio"""
    normalizedsound = effects.normalize(sound)
    normalizedsound.export(output_file_path, format=output_format)

if __name__ == "__main__":
    SoundNormalization()