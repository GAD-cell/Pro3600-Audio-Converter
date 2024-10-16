# Pro3600-Audio-Converter

Pro3600-Audio-Converter is a project aimed at converting audio files into musical scores using spectral analysis via the Fast Fourier Transform (FFT). The program identifies the frequencies of an audio file, even with overlapping notes, and generates visual representations of the audio spectrum's evolution over time.

## Table of Contents
- [Instructions](#instructions)
- [Current State](#current-state-of-the-program)
- [Future Developments](#future-developments)
- [Notes and Improvements](#notes-and-improvements)
- [Links and Resources](#links-and-resources)

---

## Instructions

The project is structured into several modules, each with a specific role:

### 1. **Audio_Converter**
   - Contains the main class `AC`, which implements the core functions of the conversion algorithm.
   
### 2. **__Init_AC__**
   - Initializes the program and allows for testing and setup. This is used for running various tests.

### 3. **Test_FFT_Code**
   - Tests the FFT algorithm and verifies the error rate generated when superimposing two notes.

### 4. **Sound Folder**
   - Contains `.wav` and `.mp3` files used to test the algorithm's functionality.

### 5. **Image_gen and Video_gen Folders**
   - `Image_gen` stores generated images representing the temporal evolution of the audio spectrum.
   - `Video_gen` contains videos created from these images, along with the corresponding audio to ensure the peaks align with the sound.

---

## Current State of the Program

The program currently has the following capabilities:
- **Frequency identification**: It can detect frequencies in audio files of varying lengths and with overlapping notes, using the FFT algorithm.
- **Spectral evolution images**: The program generates a sequence of images showing the temporal progression of the audio spectrum.
- **Video generation**: The generated images are compiled into a `.mp4` video with the corresponding audio to validate the accuracy of the spectral peaks.
- **Improved spectral resolution**: The second version (V2) of the analysis algorithm now intelligently segments the audio, reducing noise and improving frequency resolution to 4Hz with a window size of 0.25 seconds.

---

## Future Developments

Here are the upcoming goals and features planned for the project:
- **Harmonic detection**: An algorithm to detect harmonics and exclude them from being identified as played notes has been implemented.
- **Tempo detection**: Implementing a method to determine the tempo of the played notes.
- **FFT optimization**: Further refinement of the FFT algorithm to improve accuracy and efficiency.
- **JavaFX interface**: Creating a user-friendly JavaFX interface that will allow users to browse their computer for audio files, apply the Python algorithm, and download the output files.

---

## Notes and Improvements

- **Normalization improvement**: Initially, values were normalized for each time segment of the audio, which did not accurately represent the entire audio sequence. Now, normalization occurs only after the Fourier transforms have been completed for all audio segments.
- **Frequency smearing reduction**: When the audio was segmented into 1/FPS seconds, there was significant frequency smearing on the spectrum. This was mitigated by applying a Hann windowing function, which significantly improved spectral accuracy.
- **Offset correction**: The mean of the time signal was subtracted from the input to ensure no DC offset was passed into the FFT, which could distort the results.

---

## Links and Resources

Here are some helpful resources and references on FFT and audio spectral analysis:
- [Tektronix: Understanding FFT and Overlap Processing](https://www.tek.com/en/documents/primer/understanding-fft-overlap-processing-fundamentals-0)
- [FFT Visualization](https://dlbeer.co.nz/articles/fftvis.html)
- [Stanford CCRMA: Overlap-Add STFT Processing](https://ccrma.stanford.edu/~jos/sasp/Overlap_Add_OLA_STFT_Processing.html)
- [Physics of Music Notes](https://newt.phys.unsw.edu.au/jw/notes.html)
- [Spectral Analysis Guide](https://training.dewesoft.com/storage/pro/courses/fft-spectral-analysis.pdf)

