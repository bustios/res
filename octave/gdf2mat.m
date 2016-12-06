% Extract trials from GDF files and write them in MAT format

clc
clear
win_len = 499;

sets_dir = '../datasets/4-2b/';
labels_dir = sets_dir;
channels = [1 2 3];
num_samples = 2000;

[files] = loadPaths(sets_dir, labels_dir, '2b');

for i = 1:length(files)
    [epochs, sfreq] = readData(files{i}{1}, files{i}{2}, channels, num_samples, win_len);
    save('-mat-binary', [files{i}{1} '.mat'], 'epochs', 'sfreq', 'win_len');
end
