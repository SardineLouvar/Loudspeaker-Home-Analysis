# Analysis of a Loudspeaker using a Standard Microphone
A project where I measure and plot the frequency response of my speaker using a standard microphone. 

*This project is currently in development, and will be completed and have a corresponding report made by the 28th August 2026.*


## Running the Code
This code was created to be run on Windows 11 with Python 3.13.5

To run the code, first create a virtual environment and download all dependencies. This can be done by running the following code in the console:
```bash
python -m venv venv
venv\scripts\activate
pip install -r requirements.txt
```

Now, any of the individual files can be run using the following command:
```bash
python -m [file_name]
```


## Equipment
Measurements were recorded using a Fifine AM8 Microphone, connected to a PC using a USB cable. This microphone is specified to have a frequency response of 50-16kHz [1]. The speaker used to take measurements from is a Trumix AR7 loudspeaker, which has a specified frequency response of 50Hz-20kHz plus/minus 3dB [2]. A Trumix TM-12 Audio Interface was used to interface the loudspeaker to the PC.

## Experimental Method
A microphone was placed 50cm away from a speaker, angled so that the microphone capsule was vertically centered between the tweeter and woofer. Both the speaker and microphone were placed on a desk mat to add a small amount of padding to reduce vibration through the table that the experiment was performed on.

In an Audacity project, a chirp was generated with a sine waveform, consistent amplitude and 10 second duration. This chirp plays a monophonic sweep logarithmically from 20Hz to 20kHz. Other tracks were created to record microphone input during playback of the chirp. The clip of the waveform was set to start at exactly 5 seconds, allowing for background noise to be picked up before the measurement of the sweep began.

Three recordings were made, with those being at 50cm with a moderately quiet volume, one at 30cm at the same volume, and one at 30cm at a louder volume. After all measurements were made, all tracks were exported as mono WAV files with a sample rate of 44.1kHz and signed 16-bit PCM encoding.



## Citations
[1] Fifine. 2026. URL: https://fifinemicrophone.com/products/fifine-ampligame-am8-microphone

[2] Trumix. 2026. URL: https ://www.gear4music.com/Recording-and-Computers/Trumix-AR7-Active-Studio-Monitor-Ex-Demo/7H1
