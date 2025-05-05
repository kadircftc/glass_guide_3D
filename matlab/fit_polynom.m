function [SURF] = fit_polynom(POINTS, alpha, is_draw)

if nargin < 2
    alpha = 10;
    is_draw = false;
elseif nargin < 3
    is_draw = false;
end

% İkinci dereceden yüzey fit (z = a*x^2 + b*y^2 + c*x*y + d*x + e*y + f)
sf = fit([POINTS.x, POINTS.y], POINTS.z, 'poly33');
% sf = fit([x, y], z, 'poly22');

% figure
% plot(sf,[POINTS.x,POINTS.y],POINTS.z)

[xq, yq] = meshgrid(linspace(min(POINTS.x), max(POINTS.x), 500), ...
                    linspace(min(POINTS.y), max(POINTS.y), 500));
shp = alphaShape(POINTS.x, POINTS.y, alpha); % 10: alpha değeri — sınırın detay seviyesi
in = inShape(shp, xq, yq); % alpha shape içinde kalanlar

zq = sf(xq, yq);
zq(~in) = NaN; % Alpha shape dışında kalanları sil

%ipe diz
fitted_data.x = reshape(xq, size(xq,1)*size(xq,2), 1);
fitted_data.y = reshape(yq, size(yq,1)*size(yq,2), 1);
fitted_data.z = reshape(zq, size(zq,1)*size(zq,2), 1);

% NaN içeren indisler
INDEX_NaN = isnan(fitted_data.z);
fitted_data.x(INDEX_NaN) = [];
fitted_data.y(INDEX_NaN) = [];
fitted_data.z(INDEX_NaN) = [];

SURF.sf         = sf;
SURF.points     = fitted_data;
SURF.surfpoints.x = xq;
SURF.surfpoints.y = yq;
SURF.surfpoints.z = zq;

if is_draw
    figure;
    surf(xq, yq, zq, 'EdgeColor', 'none', 'FaceColor', [0 0 0.8]);
    view(3);
    xlabel('X'); ylabel('Y'); zlabel('Z');
    title('Alpha Shape ile Sınırlanmış Yüzey');
    camlight; lighting gouraud;

    % figure
    % plot3(fitted_data.x, fitted_data.y, fitted_data.z,'.r')
end
end