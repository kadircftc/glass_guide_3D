function [GLASS_GUIDE_3D] = combine_guide(GLASS_GUIDE_OFFSET_2_3D, ...
    GLASS_GUIDE_OFFSET_1_3D, GLASS_GUIDE_ARA_2_3D, GLASS_GUIDE_ARA_1_3D, ...
    GLASS_GUIDE_NORMAL_3D, alpha, is_draw)
% guide parçalarını birleştiriyor

if nargin < 6
    alpha   = 10;
    is_draw = false; 
elseif nargin < 7
    is_draw = false; 
end

GLASS_GUIDE_3D.x = [GLASS_GUIDE_OFFSET_1_3D.x; GLASS_GUIDE_ARA_1_3D.x;...
                    GLASS_GUIDE_NORMAL_3D.x;...
                    GLASS_GUIDE_ARA_2_3D.x;    GLASS_GUIDE_OFFSET_2_3D.x];
GLASS_GUIDE_3D.y = [GLASS_GUIDE_OFFSET_1_3D.y; GLASS_GUIDE_ARA_1_3D.y;...
                    GLASS_GUIDE_NORMAL_3D.y;...
                    GLASS_GUIDE_ARA_2_3D.y;    GLASS_GUIDE_OFFSET_2_3D.y];
GLASS_GUIDE_3D.z = [GLASS_GUIDE_OFFSET_1_3D.z; GLASS_GUIDE_ARA_1_3D.z;...
                    GLASS_GUIDE_NORMAL_3D.z;...
                    GLASS_GUIDE_ARA_2_3D.z;    GLASS_GUIDE_OFFSET_2_3D.z];

% Solid Cisim için Yüzeyler alınıyor...
GLASS_GUIDE_3D.shp = alphaShape(GLASS_GUIDE_3D.x, GLASS_GUIDE_3D.y, GLASS_GUIDE_3D.z, alpha); 


if is_draw
    figure;
    plot3(GLASS_GUIDE_3D.x, GLASS_GUIDE_3D.y, GLASS_GUIDE_3D.z, 'b.');
    xlabel('X'); ylabel('Y'); zlabel('Z');
    title('3D Glass: nokta bulutu');

    figure;
    plot(GLASS_GUIDE_3D.shp, 'FaceColor', 'green', 'FaceAlpha', 0.8, 'EdgeColor', 'none');
    axis equal; view(3); camlight; lighting gouraud;
    xlabel('X'); ylabel('Y'); zlabel('Z');
    title('3D Glass: solid görünüm');
end
end