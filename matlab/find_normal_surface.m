function [normal_sf_point] = find_normal_surface(sf, trimline, dist_1, dist_2, nSteps, is_draw)
% sf yüzeyi üzerindeki trimline eğrisinden sf yüzeyine dik normal_sf_point
% yüzeyinin nokta koordinatları oluşturuluyor. 
% dist_1:trimline eğrisinin üst tarafındaki yüzeyinin uzunluğu
% dist_2:trimline eğrisinin alt tarafındaki yüzeyinin uzunluğu
% nSteps: % normal yönündeki örnek sayısı

if nargin < 5
    nSteps            = 100; 
    is_draw           = false;
elseif nargin < 6
    is_draw           = false; 
end

% sf yüzeyinin trimline eğrisi üzerindeki Normal vektörü (nx, ny, nz)
[dzdx, dzdy] = differentiate(sf, trimline.x, trimline.y);
nx = -dzdx;
ny = -dzdy;
nz = ones(size(nx));
norms = sqrt(nx.^2 + ny.^2 + nz.^2);
nx = nx ./ norms;
ny = ny ./ norms;
nz = nz ./ norms;

% figure
% quiver3(trimline.x, trimline.y, trimline.z, nx, ny, nz, 0.5, 'r')
% hold on
% plot3(trimline.x, trimline.y, trimline.z, 'k.')

nPoints = length(trimline.x);

V = linspace(-dist_2, dist_1, nSteps);
[Xs, Vs] = meshgrid(1:nPoints, V);

newX = trimline.x(Xs) + nx(Xs).*Vs;
newY = trimline.y(Xs) + ny(Xs).*Vs;
newZ = trimline.z(Xs) + nz(Xs).*Vs;

%ipe diz
normal_sf_point.x = reshape(newX, nSteps*nPoints, 1);
normal_sf_point.y = reshape(newY, nSteps*nPoints, 1);
normal_sf_point.z = reshape(newZ, nSteps*nPoints, 1);

if is_draw
    figure
    plot3(normal_sf_point.x, normal_sf_point.y, normal_sf_point.z, 'g.')
end

end