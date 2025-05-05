clear
clc

% stp dosyasından üretilen nokta bulutu
data = readtable('face_upper_glass.csv');

figure
plot3(data.X, data.Y, data.Z,'Marker','.','LineStyle','none')
xlabel('X'); ylabel('Y'); zlabel('Z');

% polinom yüzeyine uydurma
[SURF_glass] = fit_polynom([zeros(size(data, 1),1), data{:,:}], 20); % alpha = 5;
