import time
from os import makedirs

import numpy as np
from sklearn.metrics import accuracy_score, cohen_kappa_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC, SVC 

import util
from feature_extraction import create_fbcsp


args = util.parse_args()
loader = util.Loader(args.d, dataset_dir=args.d_path, labels_dir=args.l_path)
logger = util.get_logger("TEST__%s" % args.d)

# Configuration paramenters 
win_len = 2  # Window size
C = 0.04

estimator = LinearSVC(C=C)
n_components = 2  # Number of components in CSP
start_time = 3.5  # Window start time for training
train_sessions = [[1, 3], [1, 2, 3], [1, 2, 3], [3], [3], [3], [3], [3], [3]]
test_sessions = [4, 5]
freq_bands = [[10, 14, 20, 24], [10, 14, 20, 24], [8, 12, 18, 22], 
              [8, 12, 10, 14], [22, 26, 26, 30], [10, 14, 12, 16],
              [12, 16, 18, 22], [8, 12, 10, 14], [18, 22, 22, 26]]

logger.info("CLASSIFICATION RESULTS")
logger.info("------------")
logger.info("- Dataset = BCI Competition IV - %s" % args.d)
logger.info("- Dataset dir = %s" % args.d_path)
logger.info("- Estimator = SVM (C=%.2f)" % C)
logger.info("- Window start time for training (at sec) = %s" % start_time)
logger.info("- Window length (secs) = %s" % win_len)
logger.info("- Number of CSP components = %s" % n_components)
logger.info("")

header = "Accuracy (%) - Kappa coefficient"

start = time.time()

for subject in args.subjects:
    print("Running tests for subject %s..." % subject)
    sessions = train_sessions[subject-1]
    raw_epochs_train = loader.load_data(subject, sessions)
    raw_epochs_test = loader.load_data(subject, test_sessions)
    X_train = raw_epochs_train.window(start_time, win_len)
    y_train = raw_epochs_train.y
    y_test = raw_epochs_test.y
    
    logger.info("Subject %s, train sessions %s" % (subject, sessions))
    logger.info("Subject %s, test sessions %s" % (subject, test_sessions))

    logger.info("Selected freq. bands: %s" % freq_bands[subject-1])
    fbcsp = create_fbcsp(freq_bands[subject-1], n_components)
    clf = Pipeline([
        ('fbcsp', fbcsp),
        ('clf', estimator)
    ])
    
    clf.fit(X_train, y_train)

    n_samples = raw_epochs_test.n_samples
    scores = np.zeros((n_samples, 2))
    length = raw_epochs_test.length
    time_points = np.linspace(0, length, n_samples, endpoint=False)
    
    for i, t in enumerate(time_points):
        X_test = raw_epochs_test.window(start_time=t, win_len=-win_len)
        y_pred = clf.predict(X_test)
        scores[i, 0] = accuracy_score(y_test, y_pred) * 100
        scores[i, 1] = cohen_kappa_score(y_test, y_pred)

    filename = "%s/%s_subject_%d" % (util.LOG_DIR, args.d, subject)
    np.savetxt(filename, scores, fmt="%.3f", header=header)

    arg_max = np.argmax(scores[:, 0])
    msg = "Max. accuracy = %.3f  at time point %d"
    logger.info(msg % (scores[arg_max, 0], arg_max))
    arg_max = np.argmax(scores[:, 1])
    msg = "Max. kappa = %.3f  at time point %d"
    logger.info(msg % (scores[arg_max, 1], arg_max))
        
    logger.info("")

end = time.time()
util.log_exec_time(end-start)
