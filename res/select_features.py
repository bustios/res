import time
import warnings
from os import makedirs

import numpy as np
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

import util
from feature_extraction import create_band_list, create_fbcsp
from feature_selection import Exhaustive, Sffs


warnings.filterwarnings("ignore")

args = util.parse_args()
loader = util.Loader(args.d, dataset_dir=args.d_path, labels_dir=args.l_path)
logger = util.get_logger("FS__%s" % args.d)

# Configuration paramenters 
start_freq = 8  # First frequency of the filter bank
n_filters = 10  # Number of filters in the filter bank
band_overlap = 2  # Overlap between the filters
bandwidth = 4  # Bandwidth of each bandpass filter 
win_len = 2  # Window length
C = 0.04  # SVM C parameter

estimator = LinearSVC(C=C)
n_components = 2  # Number of components in CSP
start_time = 3.5  # Window start time for training
train_sessions = [[1, 3], [1, 2, 3], [1, 2, 3], [3], [3], [3], [3], [3], [3]]

all_bands = create_band_list(start_freq, n_filters, band_overlap, bandwidth)
fbcsp = create_fbcsp(all_bands, n_components)
all_bands = all_bands.reshape((n_filters, 2))
all_bands = all_bands.astype(str)
all_bands = np.array(["-".join(band) for band in all_bands])
fs_method = "Exhaustive search" if args.exhaustive else "SFFS"

logger.info("FREQUENCY BAND SELECTION")
logger.info("-----------------")
logger.info("- Dataset = BCI Competition IV - %s" % args.d)
logger.info("- Dataset dir = %s" % args.d_path)
logger.info("- Feature selection method = %s" % fs_method)
logger.info("- Estimator = SVM (C=%.2f)" % C)
logger.info("- Window start time (at sec) = %s" % start_time)
logger.info("- Window length (secs) = %s" % win_len)
logger.info("- Number of CSP components = %s" % n_components)
logger.info("- Number of band-pass filters = %s" % n_filters)
logger.info("- Filter bank = %s" % " ".join(all_bands))
logger.info("")

start = time.time()

for subject in args.subjects:
    print("Selecting frequency bands for subject %d..." % subject)
    sessions = train_sessions[subject-1]
    raw_epochs = loader.load_data(subject, sessions)
    X_train = raw_epochs.window(start_time, win_len)
    y_train = raw_epochs.y

    msg = "Subject %s, sessions %s: %s epochs, %s channels, %s samples x epoch"
    logger.info(msg % (subject, sessions, X_train.shape[0], X_train.shape[1], 
                       X_train.shape[2]))
    logger.info("")
    msg = "  Selected freq. bands (Hz)   | {:^15s} | {:^14s}"
    logger.info(msg.format("Kappa coef.", "Accuracy (%)"))
    logger.info("-" * 64)

    for n_bands_to_analyze in args.n:
        if args.exhaustive:
            selector = Exhaustive(estimator, n_components, n_bands_to_analyze)
        else:
            selector = Sffs(estimator, n_components, n_bands_to_analyze)

        pipe = Pipeline([
            ("feature_extractor", fbcsp),
            ("feature_selector", selector)
        ])

        pipe.fit_transform(X_train, y_train)
       
        logger.info("%-29s | %.3f +/- %.3f | %.2f +/- %.2f" 
                     % (" ".join(all_bands[selector.selected_bands]),
                        selector.kappa_score, 
                        selector.kappa_std,
                        selector.accur_score, 
                        selector.accur_std))

    logger.info("")
    
end = time.time()
util.log_exec_time(end-start)
