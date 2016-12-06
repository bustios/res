# Restricted Exhaustive Search for Frequency Band Selection in Motor Imagery Classification

This repository contains all the code used in the experiments of the paper Restricted Exhaustive Search for Frequency Band Selection in Motor Imagery Classification as well as additional information of the experiments and results, and how to reproduce them. The code of this project, hereinfater called RES, is distributed under the 3-Clause BSD license.

## Requeriments

To execute the code, it is necessary to have installed Python 3.5 and:

- Mne = 0.13.0
- Numpy = 1.11.0
- Scipy = 0.17.0
- Scikit-learn = 0.17.1

Also, you need to download the BCI Competition IV data set 2b and run the script octave/gdf2mat.m with appropriate parameters.

## Running the code

The file results/[FS__2b__2016-11-05__22-01-07.log](https://github.com/bustios/res/blob/master/results/FS__2b__2016-11-05__22-01-07.log) contains the results of the SFFS method (the frequency bands selected for each subject) in the frequency band selection phase. Run the following command to create a .log file with the same the results:

    python res/select_features.py

The file results/[FS__2b__2016-11-05__22-03-09.log](https://github.com/bustios/res/blob/master/results/FS__2b__2016-11-05__22-03-09.log) contains the results of the RES method in the frequency band selection phase. Run the following command to create a .log file with the same the results:
 
    python res/select_features.py -e -n 2

The file results/[TEST__2b__2016-11-05__22-04-50.log](https://github.com/bustios/res/blob/master/results/TEST__2b__2016-11-05__22-04-50.log) contains the results of the classification phase. Run the following command to create a .log file with the same results:

    python res/test.py
    
This command will also create a list of files (*2b_subject_X* one for each subject in the data set) in [output/results](https://github.com/bustios/res/tree/master/results) containing the time course of the accuracy scores and kappa values for all trials in the evaluation sessions (04E and 05E).

Additionally, there is a *--help* option that displays a description of the command's supported syntax and options.
