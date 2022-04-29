from scipy.signal import butter, filtfilt
import numpy as np


def calculate_wavespeed(Acc1, Acc2, leading_edges, sf=100000, tf=50,
                        iad=0.009, cxwl=0.01):
    """ Computes wavespeed based on two Accelerometer signals and the
    timepoint of tapper excitation.

    Optional parameters include the accelerometer sampling frequency sf,
    the tapping frequency tf, the window-length that shall be regarded
    for the cross-correlation cxwl and
    the inter-accelerometer distance iad. """

    # Accelerometer data were band-pass filtered (150–1000 Hz) using a
    # second-order, zero-lag, Butterworth filter to isolate the signal
    # associated with induced shear waves.
    b, a = butter(2, [150, 1000], btype='bandpass', fs=sf)
    Acc1_filt = filtfilt(b, a, Acc1)
    Acc2_filt = filtfilt(b, a, Acc2)

    # Data were segmented into 20 ms windows starting at each leading
    # edge of the tapper excitation signal.
    win_len = int(1 / tf * sf)
    Acc1_segm = np.zeros((win_len, len(leading_edges)))
    Acc2_segm = np.copy(Acc1_segm)
    for n, edge in enumerate(leading_edges):
        edge = int(edge * sf)
        Acc1_segm[:, n] = Acc1_filt[edge:edge+win_len]
        Acc2_segm[:, n] = Acc2_filt[edge:edge+win_len]

    # Within each window, data from each accelerometer were
    # mean-centered,
    Acc1_mc = Acc1_segm - np.mean(Acc1_segm, axis=0)
    Acc2_mc = Acc2_segm - np.mean(Acc2_segm, axis=0)

    # normalized to the maximum absolute magnitude,
    Acc1_n = Acc1_mc / np.max(np.abs(Acc1_mc), axis=0)
    Acc2_n = Acc2_mc / np.max(np.abs(Acc2_mc), axis=0)

    # squared to enhance peak magnitudes,and multiplied by the sign of
    # the original measurement to preserve the wave shape.
    Acc1_sq = Acc1_n ** 2 * np.sign(Acc1_n)
    Acc2_sq = Acc2_n ** 2 * np.sign(Acc2_n)

    # Subsequently, the inter-accelerometer lag in wave arrival time was
    # determined by finding the lag that maximized the cross-correlation
    # between each windowed accelerometer signal.
    lags = np.zeros(Acc1_sq.shape[1])
    cxwl = int(cxwl*sf)
    for n in range(Acc1_sq.shape[1]):
        xc = np.correlate(Acc1_sq[:cxwl, n], Acc2_sq[:cxwl, n], 'full')

        # Cosine interpolation of the normalized cross-correlation functions
        # was used to estimate the location of peak crosscorrelation with
        # sub-frame accuracy (Cespedes, 1995).
        xc_n = xc / np.max(np.abs(xc))  # normalize x-cor array
        # find three largest values --> largest and one before and after
        y1 = np.max(xc_n)
        y0 = xc_n[np.argmax(xc_n)-1]
        y2 = xc_n[np.argmax(xc_n)+1]
        af = np.arccos((y0 + y2) / (2 * y1))  # angular frequency
        theta = np.arctan((y0 - y2) / (2 * y1 * np.sin(af)))  # phase
        offset = -theta / af  # offset as fraction of sample

        lags[n] = len(xc) / 2 - np.argmax(xc) - offset

    # Finally, wave speed was calculated by dividing the fixed
    # inter-accelerometer distance by the computed interaccelerometer
    # time lag.
    ws = iad / (lags / sf)

    return ws
