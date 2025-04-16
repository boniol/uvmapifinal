import onnxruntime
import numpy as np
import librosa
import soundfile as sf
import os

def separate_vocals(input_path, output_path):
    model_path = "models/UVR-MDX-NET-Inst_HQ_3.onnx"
    session = onnxruntime.InferenceSession(model_path)

    audio, sr = librosa.load(input_path, sr=44100, mono=True)
    audio = audio.astype(np.float32)
    audio = np.expand_dims(audio, axis=0)

    ort_inputs = {session.get_inputs()[0].name: audio}
    ort_outs = session.run(None, ort_inputs)

    sf.write(output_path, ort_outs[0][0], sr)
