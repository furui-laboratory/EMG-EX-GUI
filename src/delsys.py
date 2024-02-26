import sys
import numpy as np
from scipy import signal


from .pytrigno import TrignoEMG

class DataHandle:
    """
    Data handle class for Delsys Trigno.

    Parameters
    ----------
    n_channels : int
        Number of channels to be used. Each normal or frex or mini sensor has a 
        single EMG channel. Only a quattro sensor has four EMG channels. 

    lowchan : int, optional (default=0)
        Initial number of the channel to be used.
        Channels from `lowchan` to `lowchan + n_channel - 1` are the target of 
        recording.

    fs : float, optinal (default=2000)
        Sampling rate (Hz).
    
    samples_per_read : int, optional (default=40)
        Number of samples per channel to read in each read operation.

    order_notch : int, optinal (default=2)
        Order of a notch filter that removes hum noise from EMG signals.

    low_cut_notch : float, optinal (default=58)
        Low cut-off frequency (Hz) of the notch filter.

    high_cut_notch : float, optional (default=62)
        High cut-off frequnecy (Hz) of the notch filter.

    order_lpf : int, optional (default=2)
        Order of a low-pass filter that smoothes the EMG signals.

    low_cut_lpf : float, optional (default=2)
        Low cut-off frequency (Hz) of the low-pass filter.
    
    """
    def __init__(self, n_channels, lowchan=0, fs=2000, samples_per_read=40,
                 order_notch=2, low_cut_notch=58, high_cut_notch=62, 
                 order_lpf=2, low_cut_lpf=2):
        self.n_channels = n_channels
        self.lowchan = lowchan
        self.fs = fs
        self.sample_per_read = samples_per_read

        self._initialize_notch(order=order_notch, low_cut=low_cut_notch, 
                              high_cut=high_cut_notch)
        self._initialize_lpf(order=order_lpf, low_cut=low_cut_lpf)

    def initialize_delsys(self):
        """Initialization for Delsys Trigno system.
        """
        self.dev = TrignoEMG(
            channel_range=(self.lowchan, self.lowchan+self.n_channels-1), 
            samples_per_read=self.sample_per_read, host="localhost"
            )
        self.dev.start()
        print("prepared.")

    def stop_delsys(self):
        """Stop for Delsys Trigno system.
        """
        self.dev.stop()
        self.dev.__del__()
        print("Stop.")

    def get_emg(self, mode='raw'):
        """Get EMG signals.

        Parameters
        ----------
        mode : {'raw', 'notch', 'rect', 'lpf'}, optional
            Processing mode for EMG signal. If 'raw', the raw data are returned.
            If 'notch', the data are returned after applying the notch filter. 
            If 'rect', the rectified data are returned. If 'lpf', rectified-
            smoothed data via the low-pass filter are returned.

        Return
        ------
        EMG signal : array-like of shape=(self.sample_per_read, self.n_channels)
            
        """
        data = self.dev.read()
        rawEMG = data.T

        if mode == 'raw':
            return rawEMG
        elif mode == 'notch':
            return self._get_notched_emg(rawEMG)
        elif mode == 'rect':
            return self._get_rectified_emg(rawEMG)
        elif mode == 'lpf':
            return self._get_rectified_lpf_emg(rawEMG)
        else:
            print('Error: undefined mode', file=sys.stderr)
            sys.exit(1)


    def _get_notched_rectified_lpf_emg(self, rawEMG):
        """Get norched and rectified and smoothed EMG"""
        notched_emg = self._notch(rawEMG)
        rectifiedEMG = np.abs(notched_emg)
        return self._lpf(rectifiedEMG)
    

    def _get_rectified_emg(self, rawEMG):
        """Get rectified EMG
        """
        return np.abs(rawEMG)

    def _get_rectified_lpf_emg(self, rawEMG):
        """Get rectified and smoothed EMG
        """
        rectifiedEMG = np.abs(rawEMG)
        return self._lpf(rectifiedEMG)

    def _get_notched_emg(self, rawEMG):
        """Get notched EMG
        """
        return self._notch(rawEMG)

    def _initialize_notch(self, order, low_cut, high_cut):
        """Initialization for the notch filter
        """
        # Nyquist frequency
        nyq = (self.fs / 2)

        f_low = low_cut / nyq
        f_high = high_cut / nyq
        Wn = [f_low, f_high]

        self.b_notch, self.a_notch = signal.butter(order, Wn, 'bandstop')
        self.z_notch = np.zeros((max(len(self.a_notch), len(self.b_notch)) - 1, 
                                 self.n_channels))

    def _initialize_lpf(self, order, low_cut):
        """Initialization for the low-pass filter
        """
        # Nyquist frequency
        nyq = (self.fs / 2)

        w = low_cut / nyq

        self.b_lpf, self.a_lpf = signal.butter(order, w, "low")
        self.z_lpf = np.zeros((max(len(self.a_lpf), len(self.b_lpf)) - 1, 
                               self.n_channels))

    def _notch(self, data):
        """Applying the notch filter
        """
        notchedEMG, self.z_notch = \
                signal.lfilter(self.b_notch, self.a_notch, data, axis=0, 
                               zi=self.z_notch)
        return notchedEMG

    def _lpf(self, data):
        """Applying the low-pass filter
        """
        processedEMG, self.z_lpf = \
                signal.lfilter(self.b_lpf, self.a_lpf, data, axis=0, 
                               zi=self.z_lpf)
        return processedEMG