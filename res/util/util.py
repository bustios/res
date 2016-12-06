import argparse
import logging
from datetime import datetime
from os import makedirs
from os.path import isdir, isfile, join

import numpy as np
from scipy.io import loadmat

from .epochs import RawEpochs


LOG_DIR = "log"

def get_logger(name, lvl=logging.INFO):
    makedirs(LOG_DIR, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    logging.basicConfig(filename=("%s/%s__%s.log" % (LOG_DIR, name, date)),
                        format="[%(levelname)s] %(message)s",
                        level=lvl)
    logger = logging.getLogger(name)
    return logger

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("subjects", metavar="subject", nargs="*", type=int,
        default=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        help="Number of the subject")
    parser.add_argument("-e", "--exhaustive", action="store_true", 
        help=("Use an exhaustive search for feature selection. If not"
              "specified, SFFS will be used."))
    parser.add_argument("-n", default=[1, 2, 3], nargs="*", type=int, 
        help=("Number of frequency bands to analyze."))
    parser.add_argument("-d", metavar="dataset_name", default="2b", type=str, 
        help="Dataset name ('2a' or '2b'). 2b by default.")
    parser.add_argument("-d_path", default="datasets/4-2b", type=str, 
        help="Path where the dataset (*.mat files) is located.")
    parser.add_argument("-l_path", default="datasets/4-2b", type=str, 
        help="Path where the label files (*.mat files) are located.")
    return parser.parse_args()

def log_exec_time(exec_time):
    d = datetime.now()
    logging.info("-" * 32)
    logging.info("Finished at: %s" % d.strftime("%Y-%m-%d %H:%M:%S"))
    logging.info("Execution time: %d seconds" % exec_time)
    logging.info("-" * 32)


class Loader:

    def __init__(self, dataset, dataset_dir, labels_dir):
        if isdir(dataset_dir) and isdir(labels_dir):
            self.dataset = dataset
            self.dataset_dir = dataset_dir
            self.labels_dir = labels_dir
            if dataset == "2a":
                self.eeg_file = "A0{}{}.gdf.mat"
                self.label_file = "A0{}{}.mat"
            else:  # if dataset == "2b"
                self.eeg_file = "B0{}0{}{}.gdf.mat"
                self.label_file = "B0{}0{}{}.mat"
        else:
            raise NameError("Directory '%s' does not exist." % dataset_dir)

    def load_data(self, subject, sessions):
        X, y = [], []
        for s in sessions:
            _X, _y, sfreq, start_at = self.load_session(subject, s)
            X.append(_X)
            y.append(_y)
        X, y = np.concatenate(tuple(X)), np.concatenate(tuple(y))
        return RawEpochs(X, y, sfreq, start_at)

    def load_session(self, subject, session):
        if self.dataset == "2a":
            typ = "T" if session == 1 else "E"
            fps = self.eeg_file.format(subject, typ)
            fpl = self.label_file.format(subject, typ)
        else:  # if dataset == "2b"
            typ = "T" if session < 4 else "E"
            fps = self.eeg_file.format(subject, session, typ)
            fpl = self.label_file.format(subject, session, typ)

        session_path = join(self.dataset_dir, fps)
        labels_path = join(self.labels_dir, fpl)

        if not isfile(session_path): 
            raise NameError("File '%s' does not exist" % session_path)
        if not isfile(labels_path):
            raise NameError("File '%s' does not exist" % labels_path)

        return self._load_mat_files(session_path, labels_path)

    def _load_mat_files(self, epochs_file, labels_file):
        data = loadmat(epochs_file)
        X = data["epochs"]  # numpy array of epochs
        sfreq = data["sfreq"][0][0]  # sampling frequency
        y = loadmat(labels_file)
        y = y["classlabel"]  # epochs' class labels
        y = np.reshape(y, y.size)
        # the epochs start 'win_len' samples before the first sample to be
        # classified
        start_at = int(data["win_len"][0][0])
        return X, y, sfreq, start_at
