import matplotlib.colors as mcolors
import colormaps as cmaps
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 8
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from datetime import datetime, timedelta
import pytz, time
import os
import re
import copy
import goes2go as g2g
from toolbox.wind import spddir_to_uv
from toolbox.cartopy_tools_OLD import common_features, pc
from paint.standard2 import cm_wind
#==================== Setting up time reference variables ====================
utc = pytz.timezone('UTC') # UTC timezone
utcm5 = pytz.timezone('America/Lima') # UTC-5 timezone

#==================== Creating georeferenced variables ====================
map_proj_pc = ccrs.PlateCarree(), "PlateCarree projection"
# Add coastlines feature
coastlines_feature = cfeature.NaturalEarthFeature(
    category='physical',
    name='coastline',
    scale='50m',
    edgecolor='black',
    facecolor='none')
# Add country boundaries feature
countries_feature = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_0_countries',
    scale='50m',
    edgecolor='black',
    facecolor='none')
# Create the polygon representing the bounding box
PeruLimits_deg = [-85, -67.5, -20.5, 1.0] # Define the coordinates of the bounding box around Peru
peru_box = Polygon([(PeruLimits_deg[0], PeruLimits_deg[2]), (PeruLimits_deg[1], PeruLimits_deg[2]), (PeruLimits_deg[1], PeruLimits_deg[3]), (PeruLimits_deg[0], PeruLimits_deg[3])])
gdf_maritime = gpd.read_file("./Boundaries/World_EEZ_v11_20191118/eez_v11.shp",mask=peru_box)
gdf_states = gpd.read_file("./Boundaries/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp",mask=peru_box)
# Filter the GeoDataFrame to keep only rows where adm1_code matches "PER"
gdf_peru_land = gdf_states[gdf_states["adm1_code"].str[:3] == "PER"]
gdf_peru_sea = gdf_maritime[gdf_maritime["TERRITORY1"] == "Peru"].iloc[[1]]


def definingColormaps(disp=True):
    # Defining RGB values for RRQPEF colormap
    rgb_values = [
        [127, 127, 127],
        [0, 200, 255],
        [0, 163, 255],
        [0, 82, 255],
        [0, 0, 200],
        [150, 255, 150],
        [50, 200, 50],
        [0, 130, 0],
        [255, 255, 0],
        [170, 170, 0],
        [255, 127, 0],
        [200, 70, 70],
        [255, 160, 160],
        [255, 0, 0],
        [157, 0, 157],
        [0, 0, 0],
        [222, 222, 222]]
    # Normalize the RGB values to the range [0, 1]
    colors = [tuple(rgb / 255.0 for rgb in rgb_value) for rgb_value in rgb_values]
    # Create the colormap
    RRQPEcmap = mcolors.ListedColormap(colors)
    RRQPEcmap.set_bad('w', alpha=0)
    colormaps = {
        'ABI-L2-DSRF':'turbo',
        'ABI-L2-ACMF': cmaps.greys_light, # Clear Sky Mask
        'ABI-L2-TPWF':'Greens',
        'ABI-L2-LSTF':'jet', # Land Surface Temperature
        'ABI-L2-RRQPEF': cmaps.deep,
        "ABI-L2-ACHAF": cmaps.GMT_drywet, # Cloud Top Height
        "ABI-L2-ACHTF": 'jet', # Cloud Top Temperature
        'ABI-L2-ACTPF': cmaps.cosmic,
        'ABI-L2-DMWVF': 'jet',
        }
    if disp:
        display(colormaps)
    return colormaps

def get_image_params(data, identifier, satellite='goes16', destination_path='.\\GOESimages\\'):
    ImgTitle = data.attrs['title']
    format_string = '%Y-%m-%dT%H:%M:%S.%fZ'
    time_coverage_start = datetime.strptime(data.attrs['time_coverage_start'], format_string)
    time_coverage_end = datetime.strptime(data.attrs['time_coverage_end'], format_string)
    ImgTime = time_coverage_start + (time_coverage_end - time_coverage_start) / 2
    ImgTime = ImgTime.replace(tzinfo = utc)
    ImgTime = ImgTime.astimezone(utcm5)
    ImgTime_str = ImgTime.strftime('%H:%M UTC%Z %d-%m-%Y') # '%H:%M UTC %d-%b-%Y'
    varnames = list(data.data_vars.keys())
    spatial_res = data.attrs["spatial_resolution"].split()[0]
    # spatial_res = float(re.findall('\d+',spatial_res)[0])
    # Building image name format
    img_year, img_month, img_day = str(ImgTime.year), str(ImgTime.month).zfill(2), str(ImgTime.day).zfill(2)
    img_hour, img_minute = str(ImgTime.hour).zfill(2), str(ImgTime.minute).zfill(2)
    ImageName = '_'.join([satellite, identifier, img_year, img_month, img_day, img_hour, img_minute])+'.png'
    ImagePath = os.path.join(destination_path,'Products',identifier)
    ImageFullPath = os.path.join(ImagePath,ImageName)
    out = {'ImgTitle': ImgTitle,
           'ImgTime':ImgTime, 'ImgTime_str':ImgTime_str,
           'VarNames':varnames, 'SpatialResolution': spatial_res,
           'ImageName': ImageName, 'ImagePath': ImagePath, 'ImageFullPath': ImageFullPath}
    return out

def GeoColorPlot(destination_path, mode="latest", file_datetime=datetime.now(), toSave=False, toDisplay=True):
    """
    Plots a GeoColor image from GOES satellite data on PlateCarree projection.

    Inputs:
        gdata (xarray.Dataset): GOES satellite dataset.
        toSave (bool, optional): Whether to save the plot as an image file. Default is False.

    Returns:
        fig (matplotlib.figure.Figure): Figure object.
        ax (matplotlib.axes._subplots.GeoAxesSubplot): GeoAxesSubplot object.
    """
    file_datetime = file_datetime.astimezone(utc).replace(tzinfo=None)
    if(mode=="latest"):
        try: 
            gFileList = g2g.data.goes_latest(satellite='noaa-goes16', product='ABI-L2-MCMIP', domain='F', download=True, save_dir=destination_path, return_as='filelist')
            print("Getting latest available")
        except:
            try:
                print("Latest file available probably failed to download, rewriting existing...")
                gFileList = g2g.data.goes_latest(satellite='noaa-goes16', product='ABI-L2-MCMIP', domain='F', download=True, save_dir=destination_path, return_as='filelist', overwrite=False)
            except ValueError:
                try:
                    current_datetime = datetime.utcnow()
                    gFileList = g2g.data.goes_nearesttime(current_datetime, satellite='noaa-goes16', product='ABI-L2-MCMIP', domain='F', download=True, save_dir=destination_path, return_as='filelist')
                    print("Getting nearest available")
                except ValueError:
                    current_datetime = datetime.utcnow() - timedelta(hours=1)
                    gFileList = g2g.data.goes_nearesttime(current_datetime, satellite='noaa-goes16', product='ABI-L2-MCMIP', domain='F', download=True, save_dir=destination_path, return_as='filelist')
                    print("Getting nearest available 1 hour before")
    elif(mode=="timerange"):
        gFileList = g2g.data.goes_nearesttime(file_datetime,satellite='noaa-goes16', product='ABI-L2-MCMIP', domain='F', download=True, save_dir=destination_path, return_as='filelist')
    gdata = xr.open_dataset(os.path.join(destination_path,gFileList['file'][0]), engine='rasterio').isel(band=0)
    crs_obj = gdata.rio.crs
    crs_dest = map_proj_pc[0] # "EPSG:4326"
    GeoColorParams = get_image_params(gdata, identifier="GeoColor")
    ImgTime = GeoColorParams['ImgTime']
    isDay = (ImgTime.hour>5 and ImgTime.hour<18)
    print(f"Plotting {ImgTime} file as geocolor.")
    fig, ax = plt.subplots(figsize=(8, 12), subplot_kw=dict(projection=map_proj_pc[0]))
    ax.set_extent(PeruLimits_deg)
    if isDay: 
        print("It is daytime! Plotting NaturalColor image...")
        GeoColor = gdata.rgb.NaturalColor(night_IR=False).rio.write_crs(crs_obj)
        edgecolor, gridcolor = 'black', 'black'
    else: 
        print("It is nighttime! Plotting TrueColor image...")
        GeoColor = gdata.rgb.TrueColor(night_IR=True).rio.write_crs(crs_obj)
        edgecolor, gridcolor = 'white', 'darkgray'
    R, G, B = [
        GeoColor.isel(rgb=i).rio.reproject(crs_dest)
        .sel(x=slice(PeruLimits_deg[0], PeruLimits_deg[1]), y=slice(PeruLimits_deg[3], PeruLimits_deg[2]))
        for i in range(3)
    ]
    x_coords, y_coords = R.x.values, R.y.values
    RGBdata = np.dstack([R, G, B])
    ax.imshow(RGBdata, extent=(x_coords.min(), x_coords.max(), y_coords.min(), y_coords.max()), origin='upper')
    ax.add_feature(coastlines_feature, linewidth=0.75, edgecolor=edgecolor)
    ax.add_feature(countries_feature, linewidth=0.75, edgecolor=edgecolor)
    ax.add_geometries(gdf_peru_land['geometry'], crs=map_proj_pc[0], facecolor='none', edgecolor=edgecolor, linewidth=0.75)
    ax.add_geometries(gdf_peru_sea['geometry'], crs=map_proj_pc[0], facecolor='none', edgecolor=edgecolor, linewidth=0.75)
    # ax.gridlines(draw_labels=True, lw=0.75, color=gridcolor, alpha=0.7, ls='--')
    # ax.set_title("Peru image from satellite GOES\n {}".format(GeoColorParams['ImgTime_str']))
    if toSave:
        if not os.path.exists(GeoColorParams["ImagePath"]): os.makedirs(GeoColorParams["ImagePath"])
        fig.savefig(GeoColorParams["ImageFullPath"],dpi=300,bbox_inches='tight')
    if toDisplay: plt.show()
    else: plt.close()
    return fig, ax

def ProductData(FullFilePath, product, bucket='noaa-goes16'):
    """
    Extracts and processes specific product data from a GOES satellite dataset.

    Inputs:
        data (xarray.Dataset): GOES satellite dataset.
        product (str): The product identifier.

    Returns:
        data_re (xarray.DataArray): Processed data for the specified product.
        ProductParams (dict): Product parameters.
    """
    isACM = isACHA = isACTP = isACHT = isLST = isRRQPE = isDSR = isDMWV = isTPW = False
    if (product=="ABI-L2-ACMF"): isACM = True
    elif (product=="ABI-L2-ACHAF"): isACHA = True
    elif (product=="ABI-L2-ACTPF"): isACTP = True
    elif (product=="ABI-L2-ACHTF"): isACHT = True
    elif (product=="ABI-L2-LSTF"): isLST = True
    elif (product=="ABI-L2-RRQPEF"): isRRQPE = True 
    elif (product=="ABI-L2-DSRF"): isDSR = True
    elif (product=="ABI-L2-DMWVF"): isDMWV = True
    elif (product=="ABI-L2-TPWF"): isTPW = True
    identifier = product.split("-")[-1][:-1]
    
    if isDMWV:
        data_re = xr.open_dataset(FullFilePath, engine='netcdf4')
        ProductParams = get_image_params(data_re, identifier)
    else:
        data = xr.open_dataset(FullFilePath, engine='rasterio')
        ProductParams = get_image_params(data, identifier)
        if isACHA or isACTP or isACHT or isLST or isRRQPE or isDSR or isTPW: varname = ProductParams["VarNames"][0]
        elif isACM: varname = ProductParams["VarNames"][1]
        
        data = data.isel(band=0)[varname]
        data_re = data.rio.reproject(map_proj_pc[0], resolution=1/111.32)
        data_re = data_re.sel(x=slice(PeruLimits_deg[0], PeruLimits_deg[1]), y=slice(PeruLimits_deg[3], PeruLimits_deg[2]))
        if isACM:
            mask = ((data_re.values == 0) | (data_re.values == 1))
            data_re.values[mask] = np.nan
        elif isACTP or isRRQPE:
            mask = (data_re.values == 0)
            data_re.values[mask] = np.nan
        elif isACHT or isLST:
            data = data - 273.15
    
    return data_re, ProductParams

def ProductPlot(data_re, product, axGeo, ProductParams, toSave=False):
    """
    Plots a processed product data from a GOES satellite dataset.

    Inputs:
        data_re (xarray.DataArray): Processed data for the specified product.
        product (str): The product identifier.
        axGeo (matplotlib.axes._subplots.GeoAxesSubplot): Matplotlib axis for plotting.
        ProductParams (dict): Product parameters.
        toSave (bool, optional): Whether to save the plot as an image file. Default is False.

    Returns:
        figProd (matplotlib.figure.Figure): The figure containing the plot.
    """
    isACM = isACHA = isACTP = isACHT = isLST = isRRQPE = isDMWV = isTPW = False
    if (product=="ABI-L2-ACMF"): isACM = True
    elif (product=="ABI-L2-ACHAF"): isACHA = True
    elif (product=="ABI-L2-ACTPF"): isACTP = True
    elif (product=="ABI-L2-ACHTF"): isACHT = True
    elif (product=="ABI-L2-LSTF"): isLST = True
    elif (product=="ABI-L2-RRQPEF"): isRRQPE = True 
    elif (product=="ABI-L2-DMWVF"): isDMWV = True
    elif (product=="ABI-L2-TPWF"): isTPW = True
    
    colormaps = definingColormaps(False)
    product_cmap = colormaps[product]
    
    axProd = copy.deepcopy(axGeo)
    cbar_fontsize = 10
    if isACM or isACTP:
        flag_values = data_re.flag_values
        flag_meanings = data_re.flag_meanings.split(" ")
        nbin = len(flag_values)
        im = axProd.pcolormesh(data_re.x, data_re.y, data_re.values, cmap=product_cmap.discrete(nbin), vmin=flag_values[0], vmax=flag_values[-1])
        cbar = plt.colorbar(im,ax=axProd, orientation='horizontal', shrink=0.7, pad=0.01)
        cbar.set_ticks(flag_values)
        cbar.set_ticklabels(flag_meanings)
        # units_latex = re.sub(r'(\w)(-)(\d)', r'\1^{-\3}', data_re.units)
        cbar.set_label(r"{}".format(data_re.long_name), size=cbar_fontsize)
    elif isACHA or isACHT or isLST or isRRQPE or isTPW:
        im = axProd.pcolormesh(data_re.x, data_re.y, data_re.values, cmap=product_cmap)
        cbar = plt.colorbar(im,ax=axProd, orientation='horizontal', shrink=0.7, pad=0.01)
        units_latex = re.sub(r'(\w)(-)(\d)', r'\1^{-\3}', data_re.units)
        cbar.set_label(r"{} $({})$".format(data_re.long_name,units_latex), size=cbar_fontsize)
    elif isDMWV:
        # Convert GOES wind speed and direction to u- and v-wind components
        gu, gv = spddir_to_uv(data_re.wind_speed, data_re.wind_direction)
        im = axProd.quiver(
            data_re.lon.data,
            data_re.lat.data,
            gu.data,
            gv.data,
            data_re.wind_speed,
            **cm_wind().cmap_kwargs,
            scale=30, scale_units='xy', angles='xy',
            transform=pc
        )
        # axProd.gridlines(draw_labels=False, lw=0.75, color='darkgray', alpha=0.7, ls='--')
        cbar = plt.colorbar(im,ax=axProd, orientation='horizontal', shrink=1, pad=0.01)
        units_latex = re.sub(r'(\w)(-)(\d)', r'\1^{-\3}', data_re.wind_speed.units)
        cbar.set_label(r"{} $({})$".format(data_re.wind_speed.long_name,units_latex), size=cbar_fontsize)
    # cbar.set_label(label="asa",size=12)
    cbar.ax.tick_params(labelsize=cbar_fontsize)
    axProd.set_title(f"{ProductParams['ImgTime_str']}", loc="right")
    axProd.set_title(ProductParams['ImgTitle'], loc='left', fontweight='bold')
    # axProd.set_title("Peru image from satellite GOES\n {}".format(ProductParams['ImgTime_str']))
    
    if toSave:
        if not os.path.exists(ProductParams["ImagePath"]): os.makedirs(ProductParams["ImagePath"])
        axProd.figure.savefig(ProductParams["ImageFullPath"],dpi=300,bbox_inches='tight')
    plt.close()
    figProd = axProd.figure
    return figProd


def plotBothProjections(data,global_variables):
    variable_names = ['data','imgExtention', 'coords', 'map_proj_src','varname','product_cmap',
                      'coastlines_feature','countries_feature','map_proj_dst']
    # for var in variable_names:
    #     # exec(var+" = global_variables.get('"+var+"')")
    #     print(var+" = global_variables.get('"+var+"')")
    data = global_variables.get('data')
    imgExtention = global_variables.get('imgExtention')
    coords = global_variables.get('coords')
    map_proj_src = global_variables.get('map_proj_src')
    varname = global_variables.get('varname')
    product_cmap = global_variables.get('product_cmap')
    coastlines_feature = global_variables.get('coastlines_feature')
    countries_feature = global_variables.get('countries_feature')
    map_proj_dst = global_variables.get('map_proj_dst')
    extent_deg = np.copy(imgExtention)
    if(coords == "xy"):
        fig = plt.figure(figsize=(10, 8))
        ax1 = fig.add_subplot(1, 2, 1, projection=map_proj_src[0])
        extent_deg = ax1.get_extent()
        im1 = ax1.imshow(data[varname].values, transform=map_proj_src[0], extent=extent_deg, origin='upper', cmap=product_cmap)
        ax1.add_feature(coastlines_feature, linewidth=0.75)
        ax1.add_feature(countries_feature, linewidth=0.75)
        ax1.gridlines(draw_labels=True,lw=0.75,color='k',alpha=0.75,ls='--')
        ax1.set_title("Original image: "+map_proj_src[1],verticalalignment='bottom')

        ax2 = fig.add_subplot(1, 2, 2, projection=map_proj_dst[0])
        ax2.set_extent(imgExtention) # ax.set_global(), imgExtention, PeruLimits_deg
        extent_deg = ax2.get_extent()
        im2 = ax2.imshow(data[varname].values, transform=map_proj_src[0], origin='upper', cmap=product_cmap)
        ax2.add_feature(cfeature.BORDERS)
        ax2.add_feature(cfeature.COASTLINE)
        ax2.gridlines(draw_labels=True,lw=0.75,color='k',alpha=0.75,ls='--')
        ax2.set_title("Transformed image: "+map_proj_dst[1])
        plt.show()
        plane_projection_data = im2.get_array().data
    elif(coords == "lonlat"):
        lon, lat = data.lon.values, data.lat.values
        fig = plt.figure(figsize=(10, 8))
        
        ax1 = fig.add_subplot(1, 2, 1, projection=map_proj_src[0])
        im1 = ax1.pcolormesh(lon,lat,data[varname].values,cmap=product_cmap)
        ax1.add_feature(coastlines_feature, linewidth=0.75)
        ax1.add_feature(countries_feature, linewidth=0.75)
        ax1.gridlines(draw_labels=True,lw=0.75,color='k',alpha=0.75,ls='--')
        ax1.set_title("Original image: "+map_proj_src[1])

        ax2 = fig.add_subplot(1, 2, 2, projection=map_proj_dst[0])
        im2 = ax2.pcolormesh(lon,lat,data[varname].values, transform=map_proj_src[0],cmap=product_cmap)
        ax2.add_feature(cfeature.BORDERS)
        ax2.add_feature(cfeature.COASTLINE)
        ax2.gridlines(draw_labels=True,lw=0.75,color='k',alpha=0.75,ls='--')
        ax2.set_title("Transformed image: "+map_proj_dst[1])
        plt.show()
        plane_projection_data = data[varname].values
    return plane_projection_data, extent_deg

def plotSatImg(data,global_variables):
    variable_names = ['data','imgExtention', 'coords', 'map_proj_src','varname','product_cmap',
                      'coastlines_feature','countries_feature','map_proj_dst']
    # for var in variable_names:
    #     # exec(var+" = global_variables.get('"+var+"')")
    #     print(var+" = global_variables.get('"+var+"')")
    data = global_variables.get('data')
    imgExtention = global_variables.get('imgExtention')
    coords = global_variables.get('coords')
    map_proj_src = global_variables.get('map_proj_src')
    varname = global_variables.get('varname')
    product_cmap = global_variables.get('product_cmap')
    coastlines_feature = global_variables.get('coastlines_feature')
    countries_feature = global_variables.get('countries_feature')
    map_proj_dst = global_variables.get('map_proj_dst')
    selected_product = global_variables.get('selected_product')
    gdf_peru_land = global_variables.get('gdf_peru_land')
    gdf_peru_sea = global_variables.get('gdf_peru_sea')
    str_ImgTime = global_variables.get('str_ImgTime')
    map_proj_pc = global_variables.get('map_proj_pc')
    satellite = global_variables.get('satellite')
    year = global_variables.get('year')
    month = global_variables.get('month')
    day = global_variables.get('day')
    hour = global_variables.get('hour')
    minute = global_variables.get('minute')
    FilePath = global_variables.get('FilePath')
    PeruLimits_deg = global_variables.get('PeruLimits_deg')
    
    if(coords == "xy"):
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection=map_proj_dst[0]))
        ax.set_extent(PeruLimits_deg)
        # im = ax.imshow(transformed_data, origin='lower', transform=map_proj_dst[0], extent=extent_deg, cmap='turbo')
        im = ax.imshow(data[varname].values, transform=map_proj_src[0], cmap=product_cmap)
        cbar = plt.colorbar(im,ax=ax, orientation='horizontal', shrink=0.5, pad=0.05)
        units_latex = re.sub(r'(\w)(-)(\d)', r'\1^{-\3}', data[varname].units)
        if ( selected_product[:-1] == "ABI-L1b-Rad") or (selected_product[:-1] == "ABI-L2-CMIP"):
            cbar.set_label(r"{} $({})$, band={}".format(data.title,units_latex,selected_channel))
        else:
            cbar.set_label(r"{} $({})$".format(data.title,units_latex))
        ax.add_feature(coastlines_feature, linewidth=0.75)
        ax.add_feature(countries_feature, linewidth=0.75)
        ax.add_geometries(gdf_peru_land['geometry'], crs=map_proj_pc[0], facecolor='none', edgecolor='black', linewidth=0.75)
        ax.add_geometries(gdf_peru_sea['geometry'], crs=map_proj_pc[0], facecolor='none', edgecolor='black', linewidth=0.75)
        ax.gridlines(draw_labels=True,lw=0.75,color='k',alpha=0.7,ls='--')
        ax.set_title("GOES Image, Platform: {}, Geographic coverage: {}\n {}".format(data.platform_ID,data.scene_id,str_ImgTime))
        plt.show()
    elif(coords == "lonlat"):
        lon, lat = data.lon.values, data.lat.values
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection=map_proj_src[0]))
        im = ax.pcolormesh(lon,lat,data[varname].values,cmap=product_cmap,transform=map_proj_src[0])
        cbar = plt.colorbar(im,ax=ax, orientation='horizontal', shrink=0.5, pad=0.05)
        units_latex = re.sub(r'(\w)(-)(\d)', r'\1^{-\3}', data[varname].units)
        if ( selected_product[:-1] == "ABI-L1b-Rad") or (selected_product[:-1] == "ABI-L2-CMIP"):
            cbar.set_label(r"{} $({})$, band={}".format(data.title,units_latex,selected_channel))
        else:
            cbar.set_label(r"{} $({})$".format(data.title,units_latex))
        ax.set_extent(PeruLimits_deg)
        ax.add_feature(coastlines_feature, linewidth=0.75)
        ax.add_feature(countries_feature, linewidth=0.75)
        ax.add_geometries(gdf_peru_land['geometry'], crs=map_proj_pc[0], facecolor='none', edgecolor='black', linewidth=0.75)
        ax.add_geometries(gdf_peru_sea['geometry'], crs=map_proj_pc[0], facecolor='none', edgecolor='black', linewidth=0.75)
        ax.gridlines(draw_labels=True,lw=0.75,color='k',alpha=0.7,ls='--')
        ax.set_title("GOES Image, Platform: {}, Geographic coverage: {}\n {}".format(data.platform_ID,data.scene_id,str_ImgTime))
        plt.show()
    ImageName = satellite +'_'+ year +'_'+ month +'_'+ day +'_'+ selected_product.split('-')[-1] +'_'+ hour +'_'+ minute + '.png'
    # plt.savefig(os.path.join(FilePath, ImageName),dpi=300,bbox_inches='tight')
    print("Image '{}' saved in '{}'".format(ImageName,FilePath))
    return


