function create_3D_partial_solid_figures(GLASS_3D, GLASS_GUIDE_OFFSET_2_3D, ...
    GLASS_GUIDE_OFFSET_1_3D, GLASS_GUIDE_ARA_2_3D, GLASS_GUIDE_ARA_1_3D, ...
    GLASS_GUIDE_NORMAL_3D)

% figure;
% plot3(GLASS_3D.x, GLASS_3D.y, GLASS_3D.z, 'b.');
% hold on
% plot3(GLASS_GUIDE_OFFSET_2_3D.x, GLASS_GUIDE_OFFSET_2_3D.y, GLASS_GUIDE_OFFSET_2_3D.z, 'm.');
% plot3(GLASS_GUIDE_OFFSET_1_3D.x, GLASS_GUIDE_OFFSET_1_3D.y, GLASS_GUIDE_OFFSET_1_3D.z, 'm.');
% plot3(GLASS_GUIDE_ARA_2_3D.x, GLASS_GUIDE_ARA_2_3D.y, GLASS_GUIDE_ARA_2_3D.z, 'm.');
% plot3(GLASS_GUIDE_ARA_1_3D.x, GLASS_GUIDE_ARA_1_3D.y, GLASS_GUIDE_ARA_1_3D.z, 'm.');
% plot3(GLASS_GUIDE_NORMAL_3D.x, GLASS_GUIDE_NORMAL_3D.y, GLASS_GUIDE_NORMAL_3D.z, 'm.');
% xlabel('X'); ylabel('Y'); zlabel('Z');
% title('3D Nokta bulutu');

figure;
plot(GLASS_3D.shp, 'FaceColor', 'blue', 'FaceAlpha', 1.0, 'EdgeColor', 'none');
hold on
plot(GLASS_GUIDE_OFFSET_2_3D.shp, 'FaceColor', 'green', 'FaceAlpha', 0.7, 'EdgeColor', 'none');
plot(GLASS_GUIDE_OFFSET_1_3D.shp, 'FaceColor', 'green', 'FaceAlpha', 0.7, 'EdgeColor', 'none');
plot(GLASS_GUIDE_ARA_2_3D.shp, 'FaceColor', 'green', 'FaceAlpha', 0.7, 'EdgeColor', 'none');
plot(GLASS_GUIDE_ARA_1_3D.shp, 'FaceColor', 'green', 'FaceAlpha', 0.7, 'EdgeColor', 'none');
plot(GLASS_GUIDE_NORMAL_3D.shp, 'FaceColor', 'green', 'FaceAlpha', 0.7, 'EdgeColor', 'none');

axis equal; view(3); camlight; lighting gouraud;
xlabel('X'); ylabel('Y'); zlabel('Z');
title('3D Solid görünüm (Parçalı Glass Guide)');
end