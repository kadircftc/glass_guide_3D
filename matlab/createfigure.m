function createfigure(GLASS_POINTS, GLASS_GUIDE_POINTS, GLASS_TRIMLINE_POINTS, cizim_modu)

if nargin < 4
  cizim_modu = "nokta";
end
if cizim_modu == "nokta"
    figure1 = figure;
    axes1 = axes('Parent',figure1);
    hold(axes1,'on');
    plot3(GLASS_POINTS.x, GLASS_POINTS.y, GLASS_POINTS.z, 'Marker','.','LineStyle','none', 'DisplayName','Glass')
    hold on
    plot3(GLASS_GUIDE_POINTS.x, GLASS_GUIDE_POINTS.y, GLASS_GUIDE_POINTS.z,'Marker','.','LineStyle','none', 'DisplayName','Glass Guide')
    plot3(GLASS_TRIMLINE_POINTS.x, GLASS_TRIMLINE_POINTS.y, GLASS_TRIMLINE_POINTS.z,'Marker','*','LineStyle','none', 'DisplayName','Glass TrimLine')
    zlabel('Z');
    ylabel('Y');
    xlabel('X');
    hold(axes1,'off');
    legend(axes1,'show');
elseif cizim_modu == "yüzey"   
    tri_glass       = delaunay(GLASS_POINTS.x, GLASS_POINTS.y); % Delaunay üçgenleme
    tri_glass_guide = delaunay(GLASS_GUIDE_POINTS.x, GLASS_GUIDE_POINTS.y); % Delaunay üçgenleme

    figure1 = figure;
    axes1 = axes('Parent',figure1);
    trisurf(tri_glass, GLASS_POINTS.x, GLASS_POINTS.y, GLASS_POINTS.z, 'EdgeColor', 'none', ...
            'FaceColor', [0 0 1], 'FaceAlpha',0.5, 'DisplayName','Glass');
    hold on
    trisurf(tri_glass_guide, GLASS_GUIDE_POINTS.x, GLASS_GUIDE_POINTS.y, GLASS_GUIDE_POINTS.z, 'EdgeColor', 'none', ...
            'FaceColor', [1 0 0], 'FaceAlpha',0.5, 'DisplayName','Glass Guide');

    plot3(GLASS_TRIMLINE_POINTS.x, GLASS_TRIMLINE_POINTS.y, GLASS_TRIMLINE_POINTS.z,'Marker','*','LineStyle','none', 'DisplayName','Glass TrimLine')


    xlabel('X'); ylabel('Y'); zlabel('Z');
    view(3); % 3B bakış açısı
    hold(axes1,'off');
    legend(axes1,'show');
end