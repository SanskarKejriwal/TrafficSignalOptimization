function [funEval, best, avg] = importfile(filename, startRow, endRow)
%IMPORTFILE1 Import numeric data from a text file as column vectors.
%   FUNCTIONALEVALUATIONS = IMPORTFILE1(FILENAME)
%   Reads data from text file FILENAME for the default selection.
%
%   FUNCTIONALEVALUATIONS = IMPORTFILE1(FILENAME, STARTROW, ENDROW)
%   Reads data from rows STARTROW through ENDROW of text file FILENAME.
%
% Example:
%   FunctionalEvaluations = importfile1('run0.csv',1, 6);
%
%    See also TEXTSCAN.

% Auto-generated by MATLAB on 2022/11/30 17:47:17

%% Initialize variables.
if nargin<=2
    startRow = 1;
    endRow = inf;
end

%% Format for each line of text:
%   column1: text (%s)
% For more information, see the TEXTSCAN documentation.
formatSpec = '%s%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to the format.
% This call is based on the structure of the file used to generate this code. If an error occurs for a different file, try regenerating the code from the Import Tool.
dataArray = textscan(fileID, formatSpec, endRow(1)-startRow(1)+1, 'Delimiter', '', 'WhiteSpace', '', 'TextType', 'string', 'HeaderLines', startRow(1)-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
for block=2:length(startRow)
    frewind(fileID);
    dataArrayBlock = textscan(fileID, formatSpec, endRow(block)-startRow(block)+1, 'Delimiter', '', 'WhiteSpace', '', 'TextType', 'string', 'HeaderLines', startRow(block)-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
    dataArray{1} = [dataArray{1};dataArrayBlock{1}];
end

%% Remove white space around all cell columns.
dataArray{1} = strtrim(dataArray{1});

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post processing code is included. To generate code which works for unimportable data, select unimportable cells in a file and regenerate the script.

%% Allocate imported array to column variable names
a = dataArray{:, 1};

a = a([2 4 6],:);

funEval = str2num(a(1));
funEval = funEval(2:end);
best = str2num(a(2));
avg = str2num(a(3));


