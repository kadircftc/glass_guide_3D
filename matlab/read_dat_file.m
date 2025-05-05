function [points] = read_dat_file(filename)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
fid = fopen(filename, 'r');

header = fgetl(fid);
data = textscan(fid, '%f %f %f %f', 'Delimiter', ',', 'CollectOutput', 1);
fclose(fid);

% Düğümler ve koordinatlar
node_data = data{1};

% Sadece koordinatları struct yapısına çevir...
points.x = node_data(:,2);
points.y = node_data(:,3);
points.z = node_data(:,4);
end