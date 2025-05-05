function [offset_surf_points, offset_trimline] = offset_surface(SURF, dist, trimline, is_draw)
% SURF (noktalar ve polinom yüzeyi) şeklinde verilmiş yüzeye dist uzaklığında offset çekiyor...

if nargin < 4
    is_draw = false; 
end

%% Yüzey noktalarının Ötelenmesi
xg = SURF.points.x;
yg = SURF.points.y;
zg = SURF.points.z;

% sf yüzeyinin üzerindeki Normal vektörleri (nx, ny, nz)
[dzdx, dzdy] = differentiate(SURF.sf, xg, yg);
nx = -dzdx;
ny = -dzdy;
nz = ones(size(nx));
norms = sqrt(nx.^2 + ny.^2 + nz.^2);
nx = nx ./ norms;
ny = ny ./ norms;
nz = nz ./ norms;

offset_surf_points.x = xg + dist * nx;
offset_surf_points.y = yg + dist * ny;
offset_surf_points.z = zg + dist * nz;

%ipe diz
% offset_surf_points.x = reshape(xg_shifted, size(xg_shifted,1)*size(xg_shifted,2), 1);
% offset_surf_points.y = reshape(yg_shifted, size(xg_shifted,1)*size(yg_shifted,2), 1);
% offset_surf_points.z = reshape(zg_shifted, size(zg_shifted,1)*size(zg_shifted,2), 1);


%% trimline noktalarının Ötelenmesi 

% sf yüzeyinin trimline eğrisi üzerindeki Normal vektörü (nx, ny, nz)
[dzdx, dzdy] = differentiate(SURF.sf, trimline.x, trimline.y);
nx = -dzdx;
ny = -dzdy;
nz = ones(size(nx));
norms = sqrt(nx.^2 + ny.^2 + nz.^2);
nx = nx ./ norms;
ny = ny ./ norms;
nz = nz ./ norms;

offset_trimline.x = trimline.x + dist * nx; 
offset_trimline.y = trimline.y + dist * ny;
offset_trimline.z = trimline.z + dist * nz;

if is_draw
    figure
    plot3(offset_surf_points.x, offset_surf_points.y, offset_surf_points.z, 'm.')
    hold on
    plot3(offset_trimline.x, offset_trimline.y, offset_trimline.z, 'r*')
end

end