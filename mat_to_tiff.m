function [ output_args ] = mat_to_tiff( fileName, gtifFileName )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here




% This script takes et output, attach geographical information and 
% saves each tile as geotiff

% Date: October 25
% Author: Manish

%% Create map info using spherical datum (2*pi*r is the circumference)
ulc_x = -20015109.354; % upper left corner x
ulc_y = 10007554.677;  % upper left corner y

% lrc_x = 20015109.354;  % lower right corner x
% lrc_y = -10007554.677;  % lower right corner y

trueScale = 4631.5;  % meter (463.31*10) (463.31 pixel is usually referred to as 500 m product)
dimVal = 240;  % each tile in 240 by 240

%% Create GeoKey structure (see http://www.remotesensing.org/geotiff/spec/geotiff6.html#6.3.1.3)
a.GTModelTypeGeoKey= 1;   % Projection Coordinate System 
a.GTRasterTypeGeoKey= 1;  % RasterPixelIsArea
a.ProjectedCSTypeGeoKey= 32767;   % user defined projection (did not find sinusoidal)
a.PCSCitationGeoKey= 'Modis Sinusoidal';  % this is useless but 
a.ProjLinearUnitsGeoKey= 9003;  % linear units in meters (double check this)

%% Load data

index = regexp(fileName, '_');

hvInfo = fileName(index(3)+1:end);

hvInfo = hvInfo(1:end-4);

hInfo = str2double(hvInfo(2:3));
vInfo = str2double(hvInfo(5:6));

%% Get x and y coordinates

xlim1 = ulc_x + hInfo*trueScale*dimVal + trueScale/2;
xlim2 = ulc_x + (hInfo+1)*trueScale*dimVal + trueScale/2;


ylim1 = ulc_y - vInfo*trueScale*dimVal - trueScale/2 ;
ylim2 = ulc_y - (vInfo+1)*trueScale*dimVal -trueScale/2 ;

%% Load data

et = load(fileName);
et = et.LEptJPL;

et(imag(et)~=0) = NaN;
et(et<0) = NaN;


%% raster size
sizeET = size(et);


%% Reference matrix

R = maprasterref();

R. XLimWorld = [xlim1, xlim2];
R. YLimWorld = [ylim2, ylim1];
R.RasterSize = sizeET;
R.ColumnsStartFrom = 'north';
R.RowsStartFrom = 'west';

gtifFileName = ['/Users/trevorjm/Desktop/tests', '/', fileName(1:end-4)];

geotiffwrite(gtifFileName, et, R, 'GeoKeyDirectoryTag', a);

