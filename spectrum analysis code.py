"""   BATCH B - GROUP 3 SP TERM PROJECT 
    AUDIO SPECTRUM ANALYZER USING PYTHON    """

#Importing Libraies
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct

i=0
f,ax = plt.subplots(2)
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,1000)
ax[0].set_ylim(-5000,5000)
ax[0].set_title("Microphone Audio Spectrum")
ax[0].set_ylabel("Input")
ax[0].set_xlabel("Time")

# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,5000)
ax[1].set_ylim(-100,100)
ax[1].set_title("Fast Fourier Transform")
ax[1].set_ylabel("Volume measured in dB")
ax[1].set_xlabel("Frequency Hz")


# Show the plot, but without blocking updates
plt.pause(0.01)
plt.tight_layout()

FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
RATE = 44100 
CHUNK = 1024 # 1024bytes of data red from a buffer
RECORD_SECONDS = 0.1

audio = pyaudio.PyAudio()

# Start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True)#,
                    #frames_per_buffer=CHUNK)

global keep_going
keep_going = True

def plot_data(in_data):    
    #audio_data = np.fromstring(in_data, np.int16) # get and convert the data to float
    audio_data = struct.unpack(str(CHUNK) + 'h', in_data)
    print("The converted Binary data into Int16: ")
    print(audio_data)
    dfft = 10.*np.log10(abs(np.fft.rfft(audio_data))) # Fast Fourier Transform, 10*log10(abs) is to scale it to dB

    # Force the new data into the plot, but without redrawing axes.
    # If uses plt.draw(), axes are re-drawn every time
    #print audio_data[0:10]
    #print dfft[0:10]
    #print
    li.set_xdata(np.arange(len(audio_data)))
    li.set_ydata(audio_data)
    li2.set_xdata(np.arange(len(dfft))*10.)
    li2.set_ydata(dfft)

    # Show the updated plot, but without blocking
    plt.pause(0.01)
    if keep_going:
        return True
    else:
        return False

# Open the connection and start streaming the data
stream.start_stream()
print ("\n+---------------------------------+")
print ("| Press Ctrl+C to Break Recording |")
print ("+---------------------------------+\n")

# Loop so program doesn't end while the stream callback's
# itself for new data
while keep_going:
    try:
        plot_data(stream.read(CHUNK))
    except KeyboardInterrupt:
        keep_going=False
    except:
        pass

# Close up shop (currently not used because KeyboardInterrupt
# is the only way to close)
stream.stop_stream()
stream.close()
print("You have terminated the stream !!!")
audio.terminate()