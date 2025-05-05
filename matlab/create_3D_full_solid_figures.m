function create_3D_full_solid_figures(GLASS_3D, GLASS_GUIDE_3D)

figure;
plot3(GLASS_3D.x, GLASS_3D.y, GLASS_3D.z, 'b.');
hold on
plot3(GLASS_GUIDE_3D.x, GLASS_GUIDE_3D.y, GLASS_GUIDE_3D.z, 'm.');
xlabel('X'); ylabel('Y'); zlabel('Z');
title('3D Nokta bulutu');

figure;
plot(GLASS_3D.shp, 'FaceColor', 'blue', 'FaceAlpha', 1.0, 'EdgeColor', 'none');
hold on
plot(GLASS_GUIDE_3D.shp, 'FaceColor', 'green', 'FaceAlpha', 0.7, 'EdgeColor', 'none');
axis equal; view(3); camlight; lighting gouraud;
xlabel('X'); ylabel('Y'); zlabel('Z');
title('3D Solid görünüm');
end