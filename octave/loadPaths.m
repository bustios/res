function [files] = loadPaths(sets_path, labels_path, dataset_name)
%LOADPATHS Loads all the file paths of the data set 'dataset_name' of the 
%          BCI Competition IV [1].
%
% Inputs:
%   sets_path   = absolute or relative directory path containing the GDF files
%   labels_path = absolute or relative directory path containing the MAT files
%   dataset     = string that indicates the dataset file paths to load.
%                  It must be '2a' or '2b'
%
% Outputs:
%    files      = cell array of dataset and label file paths
%
% Author: 
%   Paul Bustios
%
% References:
%   [1] BCI Competition IV. http://www.bbci.de/competition/iv/

if strcmp(dataset_name, '2a')

files = {
    {[sets_path 'A01T.gdf']  [labels_path 'A01T.mat']},
    {[sets_path 'A01E.gdf']  [labels_path 'A01E.mat']},
    
    {[sets_path 'A02T.gdf']  [labels_path 'A02T.mat']},
    {[sets_path 'A02E.gdf']  [labels_path 'A02E.mat']},
    
    {[sets_path 'A03T.gdf']  [labels_path 'A03T.mat']},
    {[sets_path 'A03E.gdf']  [labels_path 'A03E.mat']},
    
    {[sets_path 'A04T.gdf']  [labels_path 'A04T.mat']},
    {[sets_path 'A04E.gdf']  [labels_path 'A04E.mat']},
    
    {[sets_path 'A05T.gdf']  [labels_path 'A05T.mat']},
    {[sets_path 'A05E.gdf']  [labels_path 'A05E.mat']},
    
    {[sets_path 'A06T.gdf']  [labels_path 'A06T.mat']},
    {[sets_path 'A06E.gdf']  [labels_path 'A06E.mat']},
    
    {[sets_path 'A07T.gdf']  [labels_path 'A07T.mat']},
    {[sets_path 'A07E.gdf']  [labels_path 'A07E.mat']},
    
    {[sets_path 'A08T.gdf']  [labels_path 'A08T.mat']},
    {[sets_path 'A08E.gdf']  [labels_path 'A08E.mat']},
    
    {[sets_path 'A09T.gdf']  [labels_path 'A09T.mat']},
    {[sets_path 'A09E.gdf']  [labels_path 'A09E.mat']},
};

else % if strcmp(dataset_name, '2b') 

files = {
    % File paths of data without feedback (screening)
    {[sets_path 'B0101T.gdf']  [labels_path 'B0101T.mat']},
    {[sets_path 'B0102T.gdf']  [labels_path 'B0102T.mat']},
    
    {[sets_path 'B0201T.gdf']  [labels_path 'B0201T.mat']},
    {[sets_path 'B0202T.gdf']  [labels_path 'B0202T.mat']},
    
    {[sets_path 'B0301T.gdf']  [labels_path 'B0301T.mat']},
    {[sets_path 'B0302T.gdf']  [labels_path 'B0302T.mat']},
    
    {[sets_path 'B0401T.gdf']  [labels_path 'B0401T.mat']},
    {[sets_path 'B0402T.gdf']  [labels_path 'B0402T.mat']},
    
    {[sets_path 'B0501T.gdf']  [labels_path 'B0501T.mat']},
    {[sets_path 'B0502T.gdf']  [labels_path 'B0502T.mat']},
    
    {[sets_path 'B0601T.gdf']  [labels_path 'B0601T.mat']},
    {[sets_path 'B0602T.gdf']  [labels_path 'B0602T.mat']},
    
    {[sets_path 'B0701T.gdf']  [labels_path 'B0701T.mat']},
    {[sets_path 'B0702T.gdf']  [labels_path 'B0702T.mat']},
    
    {[sets_path 'B0801T.gdf']  [labels_path 'B0801T.mat']},
    {[sets_path 'B0802T.gdf']  [labels_path 'B0802T.mat']},
    
    {[sets_path 'B0901T.gdf']  [labels_path 'B0901T.mat']},
    {[sets_path 'B0902T.gdf']  [labels_path 'B0902T.mat']}

    % File paths of data with feedback
    {[sets_path 'B0103T.gdf']  [labels_path 'B0103T.mat']},
    {[sets_path 'B0104E.gdf']  [labels_path 'B0104E.mat']},
    {[sets_path 'B0105E.gdf']  [labels_path 'B0105E.mat']},

    {[sets_path 'B0203T.gdf']  [labels_path 'B0203T.mat']},
    {[sets_path 'B0204E.gdf']  [labels_path 'B0204E.mat']},
    {[sets_path 'B0205E.gdf']  [labels_path 'B0205E.mat']},

    {[sets_path 'B0303T.gdf']  [labels_path 'B0303T.mat']},
    {[sets_path 'B0304E.gdf']  [labels_path 'B0304E.mat']},
    {[sets_path 'B0305E.gdf']  [labels_path 'B0305E.mat']},

    {[sets_path 'B0403T.gdf']  [labels_path 'B0403T.mat']},
    {[sets_path 'B0404E.gdf']  [labels_path 'B0404E.mat']},
    {[sets_path 'B0405E.gdf']  [labels_path 'B0405E.mat']},

    {[sets_path 'B0503T.gdf']  [labels_path 'B0503T.mat']},
    {[sets_path 'B0504E.gdf']  [labels_path 'B0504E.mat']},
    {[sets_path 'B0505E.gdf']  [labels_path 'B0505E.mat']},

    {[sets_path 'B0603T.gdf']  [labels_path 'B0603T.mat']},
    {[sets_path 'B0604E.gdf']  [labels_path 'B0604E.mat']},
    {[sets_path 'B0605E.gdf']  [labels_path 'B0605E.mat']},

    {[sets_path 'B0703T.gdf']  [labels_path 'B0703T.mat']},
    {[sets_path 'B0704E.gdf']  [labels_path 'B0704E.mat']},
    {[sets_path 'B0705E.gdf']  [labels_path 'B0705E.mat']},

    {[sets_path 'B0803T.gdf']  [labels_path 'B0803T.mat']},
    {[sets_path 'B0804E.gdf']  [labels_path 'B0804E.mat']},
    {[sets_path 'B0805E.gdf']  [labels_path 'B0805E.mat']},

    {[sets_path 'B0903T.gdf']  [labels_path 'B0903T.mat']},
    {[sets_path 'B0904E.gdf']  [labels_path 'B0904E.mat']},
    {[sets_path 'B0905E.gdf']  [labels_path 'B0905E.mat']}
};

end

end

