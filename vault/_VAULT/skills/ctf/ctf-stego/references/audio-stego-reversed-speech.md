# Audio Stego — Reversed Speech / Hidden Voice (CTF recipe)

Challenge pattern: "garbled, backwards-sounding noise" / "play it and you hear
strange sound" / "spoken message hidden inside". Flag format given
(e.g. `careertiq{...}`). The trick is almost always **time-reversed speech**:
the WAV plays backward, so reversing the samples yields the spoken flag.

## Recon (always do first)
- `ffprobe` / `sox file.wav -n stat` — sample rate, channels, duration, amplitude.
  Normal PCM (no LSB/metadata payload) => the secret is the SOUND, not bytes.
- Rule out spectrogram stego FIRST: render a magnitude spectrogram
  (`scipy.fft.rfft` per window -> log -> save as PNG) and eyeball it. If it shows
  only natural harmonic bands (voiced speech) and no drawn text/QR, the message is
  spoken, not painted in the spectrogram. (Vision tool can read the PNG.)

## Reverse the audio (core step)
```python
import wave, numpy
wr=wave.open("static.wav","rb"); n=wr.getnframes(); fr=wr.getframerate()
x=np.frombuffer(wr.readframes(n), dtype=np.int16).astype(np.float32)
rev=x[::-1].astype(np.int16)
w=wave.open("reversed.wav","wb"); w.setnchannels(1); w.setsampwidth(2)
w.setframerate(fr); w.writeframes(rev.tobytes())
```
`sox static.wav reversed.wav reverse` also works. Play `reversed.wav` — it now
speaks the flag forward.

## Transcribe (the part that actually reveals the flag)
Local STT that works offline on Kali:
- **Vosk** small model (`pip install vosk`, unzip `vosk-model-small-en-us-0.15`)
  is fast but FUZZY on short CTF phrases — unreliable here ("variety grew worse
  the sound" instead of the real words). Use only for a first pass.
- **OpenAI Whisper** (`pip install openai-whisper`, loads `base` ~75MB) is far
  better. Got the flag cleanly.

### KEY TRICK: bias the decoder with `initial_prompt`
Whisper will NOT emit `{` `}` and may mishear a spelled flag. Bias it with the
known flag prefix / format from the challenge description:
```python
import whisper
m=whisper.load_model("base")
r=m.transcribe("reversed.wav", language="en", verbose=False,
               condition_on_previous_text=False,
               initial_prompt="careertiq open brace reverse the sound close brace",
               beam_size=5, best_of=5, temperature=(0.0,0.2,0.4,0.6))
print(r["text"].strip())
```
Result on this challenge: `careertiq reverse the sound` ->
flag = `careertiq{reverse_the_sound}`. Confirm with the `small` model too
(loads once, ~240MB; both agreed on the same words).

## Gotchas
- **`initial_prompt` makes Whisper hallucinate the prompt back.** Biasing the
  decoder with flag-ish text on a non-speech file returns your own prompt words
  as the "transcript": an unbiased pass returned `''` while the biased pass
  returned `"receive a message flag open brace"`. ALWAYS run one unbiased pass
  first (`initial_prompt` omitted) and treat any transcript that echoes your
  prompt as noise, not evidence.
- **Empty transcript is itself a signal.** If the unbiased pass returns `''`,
  the file is probably not speech at all. Check spectral flatness (~0 = pure
  tones), whole-file autocorrelation peaks at exact block multiples, and whether
  the tones sit on an exact frequency grid — that is the tone-grid data class,
  not this one (references/audio-tone-grid-data.md).
- Whisper downloads model weights on first `load_model()` — do it in a
  background process if the box is slow; it survives a session restart.
- 24 kHz audio: resample to 16 kHz for Vosk (`sox in.wav -r 16000 -c 1 out.wav`);
  Whisper accepts 16/24/44.1k natively. A `tempo 0.85` slowdown variant can help
  iff the speech is fast, but it did NOT change the result here.
- The flag is the AUDIBLE text. CTF convention => underscores inside braces
  (`reverse_the_sound`), not spaces. If rejected, try `reversethesound` and
  `reverse the sound` as alternates.
- Don't waste time on spectrogram text if harmonics look like normal speech —
  the message is the voice, not pixels.
