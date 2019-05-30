import wave
from io import StringIO
from marytts import MaryTTS
marytts = MaryTTS()
wavs = marytts.synth_wav('Hello World!')
wav = wave.open(StringIO.StringIO(wavs))
print (wav.getnchannels(), wav.getframerate(), wav.getnframes())
