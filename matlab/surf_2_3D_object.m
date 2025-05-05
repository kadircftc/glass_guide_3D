function [OBJ_3D] = surf_2_3D_object(SURF_obj, delta, alpha, is_draw)
% SURF_obj yüzeyini alarak delta kalınlığında 3D nesne oluşturuyor..
% Aşağı yönde (aracın iç tarafı) yönünde kalınlaştırır.
% 3D cismin sınırları için: alpha için önce büyük değer dene (örneğin 10), sonra küçült 

N     = max([round(delta/0.4), 3]); % 10; % 3D cismin katman sayısı

if nargin < 3
    alpha   = 10;
    is_draw = false; 
elseif nargin < 4
    is_draw = false; 
end

% sf yüzeyinin üzerindeki Normal vektörleri (nx, ny, nz)
[dzdx, dzdy] = differentiate(SURF_obj.sf, SURF_obj.points.x, SURF_obj.points.y);
nx = -dzdx;
ny = -dzdy;
nz = ones(size(nx));
norms = sqrt(nx.^2 + ny.^2 + nz.^2);
nx = nx ./ norms;
ny = ny ./ norms;
nz = nz ./ norms;

dist = linspace(0, -delta, N);
M = length(SURF_obj.points.x);
OBJ_3D.x = zeros(M*N,1); 
OBJ_3D.y = zeros(M*N,1);
OBJ_3D.z = zeros(M*N,1);
for n = 1:N
    OBJ_3D.x((n-1)*M + 1 : n*M) = SURF_obj.points.x + dist(n) * nx;
    OBJ_3D.y((n-1)*M + 1 : n*M) = SURF_obj.points.y + dist(n) * ny;
    OBJ_3D.z((n-1)*M + 1 : n*M) = SURF_obj.points.z + dist(n) * nz;
end

% Solid Cisim için Yüzeyler alınıyor...
OBJ_3D.shp = alphaShape(OBJ_3D.x, OBJ_3D.y, OBJ_3D.z, alpha); 


if is_draw
%     figure;
%     plot3(OBJ_3D.x, OBJ_3D.y, OBJ_3D.z, 'b.');
%     xlabel('X'); ylabel('Y'); zlabel('Z');
%     title('3D Glass: nokta bulutu');

    figure;
    plot(OBJ_3D.shp, 'FaceColor', 'blue', 'FaceAlpha', 0.8, 'EdgeColor', 'none');
    axis equal; view(3); camlight; lighting gouraud;
    xlabel('X'); ylabel('Y'); zlabel('Z');
    title('3D Glass: solid görünüm');
end
end