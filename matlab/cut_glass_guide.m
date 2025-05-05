function [offset_dist1_updated_points] = cut_glass_guide(SURF_offset_dist1, SURF_offset_cut_1, is_draw)
% SURF_offset_dist1 yüzeyini SURF_offset_cut_1 yüzeyinden itibaren
% kesiyor...

if nargin < 3
    is_draw = false; 
end

% 1. Ortak tanım aralığına göre grid oluştur
% xRange = linspace(min([SURF_offset_dist1.points.x; SURF_offset_cut_1.points.x]), ...
%                   max([SURF_offset_dist1.points.x; SURF_offset_cut_1.points.x]), 300);
% yRange = linspace(min([SURF_offset_dist1.points.y; SURF_offset_cut_1.points.y]), ...
%                   max([SURF_offset_dist1.points.y; SURF_offset_cut_1.points.y]), 300);
% [X, Y] = meshgrid(xRange, yRange);
X = SURF_offset_dist1.surfpoints.x;
Y = SURF_offset_dist1.surfpoints.y;

% 2. Yüzey değerlerini hesapla 
Z1 = SURF_offset_dist1.surfpoints.z;
Z2 = SURF_offset_cut_1.sf(X, Y);

% 3. Kesişim farkı
delta = Z1 - Z2;

% 4. Maskeleme: sf1 > sf2 olan tarafı tutmak istiyoruz
mask = delta > 0;

% 5. SURF_offset_dist1 yüzeyini bu maske ile kes
Z1_masked = Z1;
Z1_masked(~mask) = NaN;

offset_dist1_updated_points.x = reshape(X, size(X,1)*size(X,2), 1);
offset_dist1_updated_points.y = reshape(Y, size(Y,1)*size(Y,2), 1);
offset_dist1_updated_points.z = reshape(Z1_masked, size(Z1_masked,1)*size(Z1_masked,2), 1);

% NaN içeren indisler
INDEX_NaN = isnan(offset_dist1_updated_points.z);
offset_dist1_updated_points.x(INDEX_NaN) = [];
offset_dist1_updated_points.y(INDEX_NaN) = [];
offset_dist1_updated_points.z(INDEX_NaN) = [];

if is_draw
    figure;
    surf(X, Y, Z1_masked, 'EdgeColor', 'none', 'FaceColor', [0 0.6 0.0]);
    xlabel('X'); ylabel('Y'); zlabel('Z');
    title('kesişimden sonra kalan taraf');
    axis equal; view(3); camlight; lighting gouraud;

%     hold on
%     plot3(SURF_offset_dist1.points.x, SURF_offset_dist1.points.y, SURF_offset_dist1.points.z, 'r.')
%     plot3(SURF_offset_cut_1.points.x, SURF_offset_cut_1.points.y, SURF_offset_cut_1.points.z, 'g.')
end
end