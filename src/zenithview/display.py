from __future__ import annotations
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import time
import logging
import numpy as np, struct
import pyaudio
import scipy.signal as signal

PI_FACTOR = 2 * np.pi

class Display:
    """
    A class used to display a bar chart and play sound to visualize sorting algorithms.
    """

    def __init__(
        self,
        width: int,
        height: int,
        caption: str = "Display",
        algorithmName: str = None,
        background: tuple = (0, 0, 0),
        loggingLevel: int = logging.INFO,
        font: str = None,
        soundDuration: float = 0.1,
        sonification: bool = False,
        updateFactor: int = 1,
        displayRate: bool = True,
        displayTime: bool = True,
        displayIterations: bool = True,
        barColor: tuple = (255, 255, 255),
        highlightColor: tuple = (255, 0, 0),
        allowPause: bool = True,
        frameRate: int = 30,
        sampleRate: int = 44100,
        framesPerBuffer: int = 1024,
        channels: int = 1,
        format: int = pyaudio.paInt16,
        amplitude: int = 32767,
        cutoffFrequency: int = 5000,
        attack: float = 0.1, 
        decay: float = 0.2, 
        sustain: float =0.5, 
        release: float = 0.1
    ) -> None:
        """
        Initializes a display with a specified width and height, and sets up the pygame environment, sound output, and logging.

        Args:
            width (int): The width of the display in pixels. Defaults to 500.
            height (int): The height of the display in pixels. Defaults to 500.
            caption (str): The caption to be displayed on the window title bar. Defaults to "Display".
            background (tuple): The RGB color of the background. Defaults to (0, 0, 0).
            loggingLevel (int): The level of logging to be used. Defaults to logging.INFO.
            font (str): The path to the font file to be used for displaying text. Defaults to None.
            soundDuration (float): The time in seconds for each sound played. Defaults to 0.1.
            sonification (bool): Whether to play sound or not. Defaults to False.
            updateFactor (int): The number of frames to update the display for each iteration. Defaults to 1.
            displayRate (bool): Whether to display the frame rate or not. Defaults to True.
            displayTime (bool): Whether to display the time elapsed or not. Defaults to True.
            displayIterations (bool): Whether to display the number of iterations or not. Defaults to True.
            barColor (tuple): The RGB color of the bars. Defaults to (255, 255, 255).
            highlightColor (tuple): The RGB color of the highlighted bars. Defaults to (255, 0, 0).
            allowPause (bool): Whether to allow pausing the display or not. Defaults to True.
            frameRate (int): The frame rate of the display. Defaults to 30.
            sampleRate (int): The sample rate of the sound output. Defaults to 44100.
            framesPerBuffer (int): The number of frames per buffer for the sound output. Defaults to 1024.
            channels (int): The number of channels for the sound output. Defaults to 1.
            format (int): The format of the sound output. Defaults to pyaudio.paInt16.
            amplitude (int): The amplitude of the sound output. Defaults to 32767.
            cutoffFrequency (int): The cutoff frequency for the sound output. Defaults to 5000.
            attack (float): The attack time for the sound output. Defaults to 0.1.
            decay (float): The decay time for the sound output. Defaults to 0.2.
            sustain (float): The sustain time for the sound output. Defaults to 0.5.
            release (float): The release time for the sound output. Defaults to 0.1.
        """
        fll = False 
        if loggingLevel not in [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL
        ]:
            loggingLevel = logging.INFO
            fll = True

        logging.basicConfig(level=loggingLevel, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        if fll:
            logging.warning("Invalid logging level, defaulting to INFO")

        logging.info("Initializing display...")
        self.width: int = width
        self.height: int = height

        if width < 10:
            logging.warning("Display width is less than 10, defaulting to 10")
            self.width = 10
        if height < 10:
            logging.warning("Display height is less than 10, defaulting to 10")
            self.height = 10

        try:
            self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
            logging.debug("Display set with width %d and height %d", self.width, self.height)
        except Exception as e:
            logging.critical("Error initializing display. Raising exception.")
            raise Exception(f"An exception occurred while initializing the display: {e}")

        logging.debug("Setting caption to %s", caption)
        pygame.display.set_caption(caption)
        logging.debug("Caption set to %s successfully.", caption)

        logging.debug("Initializing variables and settings...")

        logging.debug("Setting background to %s", background)
        self.screen.fill(background)
        self.background: tuple = background
        self.clock = None

        logging.debug("Setting audio variables...")
        self.sampleRate = sampleRate
        self.framesPerBuffer = framesPerBuffer
        self.channels = channels
        self.format = format
        self.amplitude = amplitude
        self.cutoffFrequency = cutoffFrequency

        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.releaseTime = release

        logging.debug("Initializing sound output...")
        self.audioObject = pyaudio.PyAudio()
        self.sonification: bool = sonification
        self.output = self.audioObject.open(format=self.format,
                                            channels=self.channels,
                                            rate=self.sampleRate,
                                            output=True,
                                            frames_per_buffer=self.framesPerBuffer)

        logging.debug("Initializing clock and other variables...")

        try:
            self.clock: pygame.time.Clock = pygame.time.Clock()
            logging.debug("Clock initialized successfully.")
        except Exception as e:
            logging.error(f"An error occured while initializing the clock: {e}, program might not work properly.")

        self.last_update_time: int = 0
        self.it: int = 0
        self.start: float = time.perf_counter()
        self.snap: float = self.start
        self.t: None = None
        self.ft: bool = False  
        self.null: bool = False
        self.finishTime: float = None
        self.preprocessed: dict = {}
        self.soundDuration = soundDuration
        self.arraySnapshot: list[int] = None
        logging.debug("Information variables initialized successfully.")

        logging.debug("Initializing update variables...")

        self.frameRate: int = frameRate
        self.updateFactor: int = updateFactor
        self.displayRate: bool = displayRate
        self.displayTime: bool = displayTime
        self.displayIterations: bool = displayIterations
        self.barColor: tuple = barColor
        self.highlightColor = highlightColor
        self.allowPause: bool = allowPause
        self.lenWarn: bool = False
        self.algorithmName: str = algorithmName
        self.cache = {}

        logging.debug("Update variables initialized successfully.")

        logging.debug("Initializing font...")
        pygame.font.init()
        self.font: pygame.font.Font = pygame.font.Font(font, 12)

        logging.debug("Initializing bar surface...")
        self.bar_surface: pygame.Surface = pygame.Surface((self.width, self.height))

        logging.info("Display initialized successfully.")

    def update(
        self, 
        array: list[int], 
        invertArray: bool = False,
        inverseDelta: bool = False
        ) -> None:
        """
        Updates the display with the provided array of integers.

        Args:
            array (list[int]): The list of integers to display.

        Notes:
            The display is updated only when the specified update factor is met.
            The display rate, time elapsed, and number of iterations are displayed
            at the top of the screen, if enabled in the constructor.
            The display is paused if the user presses the space bar, if allowed
            in the constructor.
        """

        if self.null:
            logging.error("Display resources were released previously, cannot update.")
            return
        
        if self.arraySnapshot is None:
            self.arraySnapshot = array[:]

        if not isinstance(self.screen, pygame.Surface):
            logging.error("Display is not initialized, cannot update.")
            return

        current_time: int = pygame.time.get_ticks()
        self.it += self.updateFactor

        if len(array) > self.width and not self.lenWarn:
            logging.warning("Array lenght is greater than display width, some elements will be ignored.")
            self.lenWarn = True

        def process(pendingData: list, sound: bool = True) -> None:
            if inverseDelta:
                pendingData = dict(list(pendingData.items())[::-1])
            for e, attr in pendingData.items():
                bar.fill(attr[1])
                self.screen.blit(bar, attr[0])

                pygame.display.flip()

                if sound:
                    if e in self.preprocessed:
                        self.output.write(self.preprocessed[e])
                    else:
                        nw = self.sinewave(self.soundDuration, e)
                        self.preprocessed[e] = nw
                        self.output.write(nw)

                if attr[1] == self.highlightColor:
                    bar.fill(self.barColor)
                    self.screen.blit(bar, attr[0])

                    pygame.display.flip()

        if current_time - self.last_update_time > 100:
            array = array[:] # avoids modifying the original array

            if invertArray:
                array = array[::-1]

            if max(array) > self.height:
                array = self.normalize(array)

            thickness = self.thickness(len(array))
            self.last_update_time = current_time
            self.bar_surface.fill(self.background)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if event.type == pygame.KEYDOWN and self.allowPause:
                    if event.key == pygame.K_SPACE: 
                        self.pause()

            h: int = self.height
            r = 0

            ct: float = time.perf_counter() # current time
            rate: float = (ct - self.snap) / 60
            self.snap = ct
            awaitText = []
            
            self.screen.blit(self.bar_surface, (0, 0))

            if self.algorithmName is not None:
                awaitText.append(f"Algorithm: {self.algorithmName}")

            if self.displayIterations: 
                awaitText.append(f"Calls: {self.it}")
            if self.displayTime: 
                awaitText.append(f"Time elapsed: {round(ct - self.start, 10)}")
            if self.displayRate: 
                awaitText.append(f"Rate: {round(rate, 10)}")

            awaitText.append(f"ArrayLength: {len(array)}")

            information: pygame.Surface = self.font.render('     -     '.join(awaitText), True, (0, 255, 0))
            self.screen.blit(information, (0, 0))

            if self.sonification: 
                pendingData = {}

                for e, oe in zip(array, self.arraySnapshot):
                    is_changed = e != oe

                    if e not in self.cache:
                        bar = pygame.surface.Surface((thickness, e))
                        bar.fill(self.barColor)
                        self.cache[e] = bar
                    else:
                        bar: pygame.surface.Surface = self.cache[e]
                        bar.fill(self.barColor)

                    self.screen.blit(bar, (r, h - e))

                    if is_changed:
                        pendingData[e] = ((r, h - e), self.highlightColor if is_changed else self.barColor)

                    r += thickness
                pygame.display.flip()
                process(pendingData)

            else:
                pendingData = {}

                for e, oe in zip(array, self.arraySnapshot):
                    is_changed = e != oe

                    if e not in self.cache:
                        bar = pygame.surface.Surface((thickness, e))
                        bar.fill(self.barColor)
                        self.cache[e] = bar
                    else:
                        bar: pygame.surface.Surface = self.cache[e]
                        bar.fill(self.barColor)

                    self.screen.blit(bar, (r, h - e))

                    if is_changed:
                        pendingData[e] = ((r, h - e), self.highlightColor if is_changed else self.barColor)

                    r += thickness
                pygame.display.flip()
                process(pendingData, sound=False)

            if self.clock is not None:
                self.clock.tick(self.frameRate)
        self.arraySnapshot = array[:]

    def filter(self, sine_wave, sample_rate, cutoff_freq=5000):
        """
        Applies a low-pass Butterworth filter to the sine wave.

        Parameters:
            sine_wave (np.array): The generated sine wave.
            sample_rate (int): The sample rate of the audio.
            cutoff_freq (int): The cutoff frequency of the low-pass filter in Hz.

        Returns:
            np.array: The sine wave after applying the low-pass filter.
        """
        nyquist = 0.5 * sample_rate
        normal_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(1, normal_cutoff, btype='low', analog=False)
        filtered_wave = signal.filtfilt(b, a, sine_wave)
        return filtered_wave
    
    def sinewave(self, duration, frequency, attack=0.1, decay=0.2, sustain=0.5, release=0.1, sample_rate=44100, amplitude=32767):
        """
        Generates a sine wave with an attack, decay, sustain, and optional release.

        Parameters:
            duration (float): The duration of the sine wave in seconds.
            frequency (int): The frequency of the sine wave in Hz.
            attack (float, optional): Time for the attack phase in seconds. Defaults to 0.1s.
            decay (float, optional): Time for the decay phase in seconds. Defaults to 0.2s.
            sustain (float, optional): The amplitude level during the sustain phase. Defaults to 0.5.
            release (float, optional): Time for the release phase in seconds. Defaults to 0.1s.
            sample_rate (int, optional): The sample rate of the sine wave. Defaults to 44100 Hz.
            amplitude (int, optional): The amplitude of the sine wave. Defaults to 32767.

        Returns:
            bytes: The generated sine wave with the envelope applied as a sequence of 16-bit signed little-endian samples.
        """
        num_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, num_samples, endpoint=False)
        sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)

        attack_samples = min(int(attack * sample_rate), num_samples)
        decay_samples = min(int(decay * sample_rate), num_samples - attack_samples)
        sustain_samples = max(0, num_samples - attack_samples - decay_samples - int(release * sample_rate))
        release_samples = min(int(release * sample_rate), num_samples - attack_samples - decay_samples - sustain_samples)

        envelope = np.ones_like(t)

        # apply attack
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        # apply decay
        if decay_samples > 0:
            envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain, decay_samples)

        # apply sustain
        if sustain_samples > 0:
            envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain

        # apply release
        if release_samples > 0:
            envelope[attack_samples + decay_samples + sustain_samples:] = np.linspace(sustain, 0, release_samples)

        # apply the envelope to the sine wave
        sine_wave *= envelope

        filtered_wave = self.filter(sine_wave, sample_rate, self.cutoffFrequency)

        return b''.join(struct.pack('<h', int(sample)) for sample in filtered_wave)

    def preprocess(self, array: list[int]) -> dict[int, bytes]:
        """
        Preprocesses an array of integers by generating sine waves of given duration and frequency
        for each element in the array.

        Observation: The function already sends the processed data to the class, the cached data is only returned in case of inspection.

        Parameters:
            array (list[int]): The array of integers to preprocess.

        Returns:
            dict[int, bytes]: A dictionary mapping each element in the array to its corresponding
            sine wave as a sequence of 16-bit signed little-endian samples.
        """
        logging.debug(f"Preprocessing array...")
        interval = round(len(array) / 10)

        if interval == 0:
            logging.debug(f"Array length is too small, setting interval to 1.")
            interval = 1

        for i, e in enumerate(array):
            if i % interval == 0:
                logging.debug(f"Processed {i}/{len(array)}")
            self.preprocessed[e] = self.sinewave(
                duration=self.soundDuration,
                frequency=e,
                attack=self.attack,
                decay=self.decay,
                sustain=self.sustain,
                release=self.releaseTime,
                sample_rate=self.sampleRate,
                amplitude=self.amplitude,
            )

        logging.debug(f"Preprocessing complete.")
        return self.preprocessed

    def thickness(self, arrayLen: int) -> int:
        """
        Calculates the thickness of each bar based on the length of the input array.

        Args:
            arrayLen (int): The length of the array to be displayed.

        Returns:
            int: The calculated thickness of each bar, determined by dividing the display width by the array length.
        """
        return int(self.width / arrayLen)

    def pause(self, bind: int = pygame.K_SPACE, allowQuit: bool = True) -> None:
        """
        Pauses the display until the user presses a specified key.

        Args:
            bind (int, optional): The key to bind the pause/unpause action to. Defaults to pygame.K_SPACE.
            allowQuit (bool, optional): Whether to allow exiting the program when the display is paused. Defaults to True.

        Returns:
            None
        """
        paused: bool = True

        logging.info("Display paused.")
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT and allowQuit:
                    pygame.quit()
                    exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == bind:
                        logging.info("Display unpaused.")
                        paused = False

    def normalize(self, list: list[int]) -> list[int]:
        """
        Normalizes a list of integers to the display height.

        Args:
            list (list[int]): The list of integers to be normalized.

        Returns:
            list[int]: The normalized list of integers.
        """
        old_min = min(list)
        old_max = max(list)
        tmin = (self.height / 10)
        tmax = self.height - 12
                
        return [
            round(((x - old_min) / (old_max - old_min)) * (tmax - tmin) + tmin) for x in list
        ]

    def completeUpdate(self, array: list[int]) -> None:
        r = 0
        t = self.thickness(len(array))

        for e in array:
            if e in self.cache:
                b = self.cache[e]
            else:
                b = pygame.Surface((t, e))
                self.cache[e] = b
            b.fill((0, 255, 0))

            self.screen.blit(b, (r, self.height - e))

            pygame.display.flip()

            if self.sonification:
                if e in self.preprocessed:
                    self.output.write(self.preprocessed[e])
                else:
                    nw = self.sinewave(self.soundDuration, e)
                    self.preprocessed[e] = nw
                    self.output.write(nw)

            r += t

        r = 0

        for e in array:
            if e in self.cache:
                b = self.cache[e]
            else:
                b = pygame.Surface((t, e))
                self.cache[e] = b
            b.fill((255, 255, 255))

            self.screen.blit(b, (r, self.height - e))

            pygame.display.flip()

            r += t


    def release(self, lastArray: list[int] = None, update: bool = True, hold: bool = True) -> None:
        """
        Releases all resources allocated by the display and optionally holds the display.
        
        Args:
            lastArray (list[int], optional): The last array to be displayed. Defaults to None.
            update (bool, optional): Whether to update the display with the last array. Defaults to True.
            hold (bool, optional): Whether to hold the display after releasing resources. Defaults to True.
        """

        if not isinstance(self.screen, pygame.Surface):
            logging.error("Display is not initialized, cannot update.")
            return

        if lastArray is not None and update is not False:
            logging.debug("Updating last array image.")
            self.completeUpdate(lastArray)  
            logging.debug("Last array image updated successfully.")

        if hold:
            self.hold()
            logging.debug("Display held successfully.")
            
            logging.info("Releasing memory...")

            start = self.start

            del self.__dict__

            logging.debug("Finish time stored at self.finishTime for further use.")
            self.finishTime = time.perf_counter() - start
            self.null = True

            logging.info("Display finished gracefully.")

    def hold(self) -> None:
        """
        Holds the execution of the program and processes events.

        Continuously listens for events in a loop. If a QUIT event is detected,
        it exits the application and stops the loop, effectively halting the 
        execution of the program.

        Returns:
            None
        """
        running: bool = True
        logging.debug("Holding display...")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.debug("QUIT event detected, finishing display...")
                    try:
                        pygame.quit()
                    except Exception as e:
                        logging.error(f"Failed to quit pygame: {e}")
                    running = False

    def __repr__(self):
        return f"Display({self.width}, {self.height})"
    
    def __str__(self):
        return f"Display({self.width}, {self.height})"
    
    def __getattr__(self, name):
        logging.error(f"Attribute {name} not found.")
    
    def __delattr__(self, name):
        logging.debug(f"Attribute {name} was deleted.")