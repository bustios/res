function [epochs, sfreq] = readData(gdf_file, lbls_file, channels, epoch_len, win_len)
% READDATA Reads 'gdf_file' and 'lbls_file' files to extract motor imagery 
%          epochs from EEG signals.
%   This function extracts an epoch of size (channels x epoch_len) from each 
%   motor imagery trial, beginning at each motor imagery cue onset.
%   To read the GDF file format [1], it is used the SLOAD function from 
%   BIOSIG toolbox [2].
%
% Inputs:
%   gdf_file    = absolute or relative GDF file path
%   lbls_file   = absolute or relative MAT file path of trials' class labels
%   channels    = indices of the channels to be selected
%   epoch_len   = number of time points (samples) for each channel in an epoch
%   win_len     = number of time points (samples) needed to classify the first 
%                 sample in a epoch
%
% Outputs:
%    epochs     = motor imagery epochs
%    sfreq      = sampling rate
%
% Author:
%    Paul Bustios
%
% References:
%   [1] GDF - General Data Format for Biomedical Signals. 
%       https://arxiv.org/abs/cs/0608052
%   [2] BIOSIG toolbox. http://biosig.sf.net/
%
%
%  Event type    |    Description
%------------------------------------------
% 276     0x0114 |  Idling EEG (eyes open)
% 277     0x0115 |  Idling EEG (eyes closed)
% 768     0x0300 |  Start of a trial
% 769     0x0301 |  Cue onset left (class 1)
% 770     0x0302 |  Cue onset right (class 2)
% 771     0x0303 |  Cue onset foot (class 3)
% 772     0x0304 |  Cue onset tongue (class 4)
% 781     0x030D |  BCI feedback (continuous)
% 783     0x030F |  Cue unknown 
% 1023    0x03FF |  Rejected trial
% 1072    0x0430 |  Eye movement
% 1077    0x0435 |  Horizontal eye movement
% 1078    0x0436 |  Vertical eye movement
% 1079    0x0437 |  Eye rotation 
% 1081    0x0439 |  Eye blinks
% 32766   0x7FFE |  Start of a new run

TRIAL_START = 768;
REJECTED = 1023;

load(lbls_file); % load 'classlabel' variable from 'lbls_file' MAT file
[eeg, HDR] = sload(gdf_file, channels);

sfreq      = HDR.EVENT.SampleRate;
events     = HDR.EVENT.TYP;
num_events = length(events);
num_epochs = length(classlabel);
num_chanls = length(channels);
num_trial  = 0;

epochs    = zeros(num_epochs, num_chanls, epoch_len + win_len);
epoch_len = epoch_len - 1;

for i = 1:num_events
    if events(i) == TRIAL_START
        start = HDR.EVENT.POS(i);
        end_ = start + epoch_len;
        start = start - win_len;  % to classify the first sample of the trial
        num_trial = num_trial + 1;
        epochs(num_trial, :, :) = eeg(start:end_, :)';
    end
end

epochs(isnan(epochs)) = 0;

end
