clear
clc

%% Girdi parametreleri
delta_glass = 3.8; % camın kalınlığı
delta_guide = 0.1; % kanalın kalınlığı
dist_1 = 3.5;             % Camın dış (üst) taraftaki kanala uzaklığı
dist_2 = 13.1 + delta_glass;  % Camın iç (alt) taraftaki kanala uzaklığı
dist_3 = 6.2;   % Camın karşı taraftaki kanala uzaklığı
len_1 = 13.3 - delta_guide;   % Dış (üst) taraftaki kanalın uzunluğu
len_2 = 28.8 - delta_guide;  % İç (alt) taraftaki kanalın uzunluğu

alpha = 5;  % polinom uydurma aşamasında yüzeyin sınırlarını belirleme parametresi

GLASS_POINTS = read_dat_file('glass2.5kpoint.dat');
GLASS_GUIDE_POINTS = read_dat_file('glass_guide_wall2.5kpoints.dat');
% GLASS_POINTS = read_dat_file('glass10kpoint.dat');
% GLASS_GUIDE_POINTS = read_dat_file('glass_guide_wall10kpoints.dat');
GLASS_TRIMLINE_POINTS = read_dat_file('glass_trimline.dat');

% createfigure(GLASS_POINTS, GLASS_GUIDE_POINTS, GLASS_TRIMLINE_POINTS, "nokta") % "nokta" "yüzey"

% polinom yüzeyine uydurma
[SURF_glass] = fit_polynom(GLASS_POINTS, alpha);

% Normal yüzeyini bulma
[normal_sf_point] = find_normal_surface(SURF_glass.sf, GLASS_TRIMLINE_POINTS, dist_1, dist_2, 100, false);
[SURF_normal2glass] = fit_polynom(normal_sf_point, alpha); 
[offset_normal2glass_points] = offset_surface(SURF_normal2glass, dist_3, GLASS_TRIMLINE_POINTS, false);
[SURF_offset_normal2glass] = fit_polynom(offset_normal2glass_points, alpha);

% dist 1
[offset_glass_points_dist1, trimline_dist1] = offset_surface(SURF_glass, dist_1, GLASS_TRIMLINE_POINTS, false);
[SURF_offset_dist1] = fit_polynom(offset_glass_points_dist1, alpha);

% dist 2
[offset_glass_points_dist2, trimline_dist2] = offset_surface(SURF_glass, -dist_2, GLASS_TRIMLINE_POINTS, false); 
[SURF_offset_dist2] = fit_polynom(offset_glass_points_dist2, alpha);

% Ara kısımdaki kanallar
[ara_dist1_sf_point] = find_normal_surface(SURF_normal2glass.sf, trimline_dist1, dist_3, 0, 100, false);
[SURF_ara_dist1] = fit_polynom(ara_dist1_sf_point, alpha); 

[ara_dist2_sf_point] = find_normal_surface(SURF_normal2glass.sf, trimline_dist2, dist_3, 0, 100, false);
[SURF_ara_dist2] = fit_polynom(ara_dist2_sf_point, alpha); 

%% Alt ve üst glass guide kesimi
% Glass Guide'ı kesecek yüzeylere paralel normal2glass yüzeyi 
[cut_sf_point] = find_normal_surface(SURF_glass.sf, GLASS_TRIMLINE_POINTS, 1.5*dist_1, 1.5*dist_2, 100, false);
[SURF_cut] = fit_polynom(cut_sf_point, alpha); 

% Glass Guide'ın üst tarafını kesecek yüzey
[offset_cut_points_1] = offset_surface(SURF_cut, -(len_1-dist_3), GLASS_TRIMLINE_POINTS, false);
[SURF_offset_cut_1] = fit_polynom(offset_cut_points_1, alpha);

% Glass Guide'ın alt tarafını kesecek yüzey
[offset_cut_points_2] = offset_surface(SURF_cut, -(len_2-dist_3), GLASS_TRIMLINE_POINTS, false);
[SURF_offset_cut_2] = fit_polynom(offset_cut_points_2, alpha);

% Glass Guide'lar kesiliyor...
offset_dist1_updated_points = cut_glass_guide(SURF_offset_dist1, SURF_offset_cut_1, false);
[SURF_offset_dist1_updated] = fit_polynom(offset_dist1_updated_points, alpha);
offset_dist2_updated_points = cut_glass_guide(SURF_offset_dist2, SURF_offset_cut_2, false);
[SURF_offset_dist2_updated] = fit_polynom(offset_dist2_updated_points, alpha);

% 3D Glass ve 3D glass guide
GLASS_3D = surf_2_3D_object(SURF_glass, delta_glass, alpha, false);
GLASS_GUIDE_OFFSET_2_3D = surf_2_3D_object(SURF_offset_dist2_updated, delta_guide, alpha, false);
GLASS_GUIDE_OFFSET_1_3D = surf_2_3D_object(SURF_offset_dist1_updated, -delta_guide, alpha, false);
GLASS_GUIDE_ARA_2_3D = surf_2_3D_object(SURF_ara_dist2, delta_guide, alpha, false);
GLASS_GUIDE_ARA_1_3D = surf_2_3D_object(SURF_ara_dist1, -delta_guide, alpha, false);
GLASS_GUIDE_NORMAL_3D = surf_2_3D_object(SURF_offset_normal2glass, delta_guide, alpha, false);

% Parçalı Glass Guide için Çizim
create_3D_partial_solid_figures(GLASS_3D, GLASS_GUIDE_OFFSET_2_3D, ...
    GLASS_GUIDE_OFFSET_1_3D, GLASS_GUIDE_ARA_2_3D, GLASS_GUIDE_ARA_1_3D, ...
    GLASS_GUIDE_NORMAL_3D)

% Glass Guide PArçalarını Birleştirme...
GLASS_GUIDE_3D = combine_guide(GLASS_GUIDE_OFFSET_2_3D, ...
    GLASS_GUIDE_OFFSET_1_3D, GLASS_GUIDE_ARA_2_3D, GLASS_GUIDE_ARA_1_3D, ...
    GLASS_GUIDE_NORMAL_3D, 1, false); %alpha = 5;

% Full Glass Guide için Çizim
create_3D_full_solid_figures(GLASS_3D, GLASS_GUIDE_3D)


% % Glass Guide'ın nokta kümesi
% COMPLETE_GLASS_GUIDE.x = ...
%     [SURF_offset_dist2_updated.points.x; SURF_ara_dist2.points.x; ...
%      SURF_offset_normal2glass.points.x; SURF_ara_dist1.points.x; ...
%      SURF_offset_dist1_updated.points.x];
% COMPLETE_GLASS_GUIDE.y = ...
%     [SURF_offset_dist2_updated.points.y; SURF_ara_dist2.points.y; ...
%      SURF_offset_normal2glass.points.y; SURF_ara_dist1.points.y; ...
%      SURF_offset_dist1_updated.points.y];
% COMPLETE_GLASS_GUIDE.z = ...
%     [SURF_offset_dist2_updated.points.z; SURF_ara_dist2.points.z; ...
%      SURF_offset_normal2glass.points.z; SURF_ara_dist1.points.z; ...
%      SURF_offset_dist1_updated.points.z];
% figure
% plot3(COMPLETE_GLASS_GUIDE.x,COMPLETE_GLASS_GUIDE.y,COMPLETE_GLASS_GUIDE.z, ...
%     'Marker','.','LineStyle','none',...
%     'Color',[0.392156862745098 0.831372549019608 0.0745098039215686])
% hold on
% plot3(SURF_glass.points.x,SURF_glass.points.y,SURF_glass.points.z, 'b.')
% 
% figure
% plot3(SURF_offset_dist1_updated.points.x,SURF_offset_dist1_updated.points.y,...
%       SURF_offset_dist1_updated.points.z, 'r.')
