import matplotlib.colors as mcolors
import colormaps as cmaps
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 8
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import rioxarray as rxr
from datetime import datetime, timedelta
import pytz, time
import os, re, copy, requests, cv2
from unidecode import unidecode
import goes2go as g2g
from toolbox.wind import spddir_to_uv
from toolbox.cartopy_tools_OLD import common_features, pc
from paint.standard2 import cm_wind
import GOESutils.DataBaseUtils as dbu
import GOESutils.MyUtils as mutl
import GOESutils.GOESimport as gimp
from bs4 import BeautifulSoup

from IPython.display import display, Image, clear_output
#==================== Setting up time reference variables ====================
utc = pytz.timezone('UTC') # UTC timezone
utcm5 = pytz.timezone('America/Lima') # UTC-5 timezone

#==================== Creating georeferenced variables ====================
map_proj_pc = ccrs.PlateCarree(), "PlateCarree projection"
# Add coastlines feature
# coastlines_feature = cfeature.NaturalEarthFeature(
#     category='physical',
#     name='coastline',
#     scale='10m',
#     edgecolor='black',
#     facecolor='none')
# # Add country boundaries feature
# countries_feature = cfeature.NaturalEarthFeature(
#     category='cultural',
#     name='admin_0_countries',
#     scale='10m',
#     edgecolor='black',
#     facecolor='none')
# Create the polygon representing the bounding box
PeruLimits_deg = [-85, -67.5, -20.5, 1.0] # Define the coordinates of the bounding box around Peru
peru_box = Polygon([(PeruLimits_deg[0], PeruLimits_deg[2]), (PeruLimits_deg[1], PeruLimits_deg[2]), (PeruLimits_deg[1], PeruLimits_deg[3]), (PeruLimits_deg[0], PeruLimits_deg[3])])
# gdf_coastline = gpd.read_file("./Boundaries/ne_10m_coastline/ne_10m_coastline.shp", mask=peru_box)
gdf_maritime = gpd.read_file("./Boundaries/World_EEZ_v11_20191118/eez_v11.shp", mask=peru_box)
gdf_countries = gpd.read_file("./Boundaries/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp", mask=peru_box)
gdf_states = gpd.read_file("./Boundaries/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp", mask=peru_box)
gdf_peru_land = gpd.read_file("./Boundaries/PER_adm/PER_adm2.shp")
# Filter the GeoDataFrame to keep only rows where adm1_code matches "PER"
gdf_peru_sea = gdf_maritime[gdf_maritime["TERRITORY1"] == "Peru"].iloc[[1]]
gdf_countries = gdf_countries[gdf_countries["ADMIN"] != "Peru"]
gdf_states = gdf_states[gdf_states["adm1_code"].str[:3] == "PER"]
pol_lima = gdf_states[gdf_states['name'] == "Lima"].geometry.iloc[0]
pol_lima_prov = gdf_states[gdf_states['name'] == "Lima Province"].geometry.iloc[0]
pol_callao = gdf_states[gdf_states['name'] == "Callao"].geometry.iloc[0]
ind_lima = gdf_states[gdf_states['name'] == "Lima"].index[0]
gdf_states.at[ind_lima,'geometry'] = pol_lima.union(pol_callao)#.union(pol_lima_prov)
gdf_states = gdf_states[~gdf_states['name'].isin(["Callao"])]#"Lima Province", 

pol_lima = gdf_peru_land[gdf_peru_land['NAME_1'] == "Lima"].geometry.iloc[0]
pol_lima_prov = gdf_peru_land[gdf_peru_land['NAME_1'] == "Lima Province"].geometry.iloc[0]
pol_callao = gdf_peru_land[gdf_peru_land['NAME_1'] == "Callao"].geometry.iloc[0]
ind_lima = gdf_peru_land[gdf_peru_land['NAME_1'] == "Lima"].index[0]
gdf_peru_land.at[ind_lima,'geometry'] = pol_lima.union(pol_callao)#.union(pol_lima_prov)
gdf_peru_land = gdf_peru_land[~gdf_peru_land['NAME_1'].isin(["Callao"])]#"Lima Province", 
departments = gdf_peru_land["NAME_1"].unique().tolist()
departments_folder = [unidecode(d.lower().replace(" ","")) for d in departments]
departments_folder = [s[0].upper() + s[1:].lower() if s != "limaprovince" else "Limametropolitana" for s in departments_folder]

def RenameFile(filename):
    match = re.match(r"goes16_(\w+)_(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2}).png", filename)
    if match:
        product = match.group(1)
        year = match.group(2)
        month = match.group(3)
        day = match.group(4)
        hour = match.group(5)
        minute = match.group(6)
        
        # Format the extracted parts into the desired format
        newfilename = f"{product}-{year}-{month}-{day} {hour}-{minute}.png"
    else:
        print("Invalid input string format")
    return newfilename

def definingColormaps(disp=True):
    # Defining RGB values for RRQPEF colormap
    rgb_values = [[0, 0, 0], [0, 0, 250], [0, 250, 250], [67, 80, 126], [205,240,254], [120,120,120]]
    # Normalize the RGB values to the range [0, 1]
    colors = [tuple(rgb / 255.0 for rgb in rgb_value) for rgb_value in rgb_values]
    # Create the colormap
    # RRQPEcmap = mcolors.ListedColormap(colors)
    # RRQPEcmap.set_bad('w', alpha=0)
    ACTPcmap = mcolors.ListedColormap(colors)
    product_colormaps = {
        "ABI-L2-LSTF": dict(cmap='jet', min = 0, max = 45, cbar_extent="both", type="Images/Type2"), # Land Surface Temperature
        "ABI-L2-ACHAF": dict(cmap=cmaps.GMT_drywet, min = 0, max = 17, cbar_extent="max", type="Images/Type3"), # Cloud Top Height
        "ABI-L2-ACHTF": dict(cmap='jet', min = -100, max = 50, cbar_extent="both", type="Images/Type4"), # Cloud Top Temperature
        "ABI-L2-ACMF": dict(cmap=cmaps.greys_light, min = 1, max = 4, cbar_extent="neither", type="Images/Type5"), # Clear Sky Mask
        "ABI-L2-RRQPEF": dict(cmap=cmaps.deep, min = 0, max = 100, cbar_extent="max", type="Images/Type6"),#, cmaps.ncview_default
        "ABI-L2-TPWF": dict(cmap='Greens', min = 0, max = 70, cbar_extent="max", type="Images/Type7"),
        "ABI-L2-ACTPF": dict(cmap=ACTPcmap, min = 1, max = 6, cbar_extent="neither", type="Images/Type8"), # cmaps.cosmic_r 
        "ABI-L2-DSRF": dict(cmap='turbo', min = 0, max = 1000, cbar_extent="max"),
        "ABI-L2-DMWVF": dict(cmap='jet', cbar_extent="both"),
        }
    if disp:
        display(product_colormaps)
    return product_colormaps
    
def GeoColorPlot(RGBdata, GeoColorParams, toSave=False, toDisplay=False, toUpload=False, department=False, dep=None, dpi=300):
    ImageTime = GeoColorParams["ImageTime"]
    print(f"Plotting geocolor image at {ImageTime}.")
    ImageTime = GeoColorParams['ImageTime']
    isDay = (ImageTime.hour>5 and ImageTime.hour<17)
    if isDay: 
        print("It is daytime! Plotting NaturalColor image...")
        edgecolor, gridcolor = 'white', 'black'
    else: 
        print("It is nighttime! Plotting TrueColor image...")
        edgecolor, gridcolor = 'white', 'darkgray'
    x_coords, y_coords = RGBdata.x.values, RGBdata.y.values
    fig, ax = plt.subplots(figsize=(8, 12), subplot_kw=dict(projection=map_proj_pc[0]))
    # ax.set_extent(PeruLimits_deg)
    RGBdata.plot.imshow(ax=ax)
    # ax.imshow(RGBdata, extent=(x_coords.min(), x_coords.max(), y_coords.min(), y_coords.max()), origin='upper')
    # ax.add_feature(coastlines_feature, linewidth=0.75, edgecolor=edgecolor)
    # ax.add_feature(countries_feature, linewidth=0.75, edgecolor=edgecolor)
    
    if department: 
        gdf_land = gdf_peru_land[gdf_peru_land['NAME_1'] == dep][["NAME_2", "geometry"]]
        ax.add_geometries(gdf_land.geometry, crs=map_proj_pc[0], facecolor='none', edgecolor=edgecolor, linewidth=0.75)
    if not department: 
        gdf_land = gdf_states[["name","geometry"]]
        ax.add_geometries(gdf_countries['geometry'], crs=map_proj_pc[0], facecolor='none', edgecolor=edgecolor, linewidth=0.75)
        ax.add_geometries(gdf_land.geometry, crs=map_proj_pc[0], facecolor='none', edgecolor=edgecolor, linewidth=0.75)
        ax.add_geometries(gdf_peru_sea['geometry'], crs=map_proj_pc[0], facecolor='none', edgecolor=edgecolor, linewidth=0.75)
    
    for ind, row in gdf_land.iterrows():
        x_center, y_center = row.geometry.centroid.xy
        ax.annotate(row[0], (x_center[0], y_center[0]), ha="center", va="center", bbox=dict(boxstyle="round, pad=0.2", facecolor="white", alpha=0.5))
    # ax.gridlines(draw_labels=True, lw=0.75, color=gridcolor, alpha=0.7, ls='--')
    ax.set_title("")
    if toSave:
        if not os.path.exists(GeoColorParams["ImagePath"]): os.makedirs(GeoColorParams["ImagePath"])
        fig.savefig(GeoColorParams["FullImageName"],dpi=dpi,bbox_inches='tight')
        
    if toDisplay: plt.show()
    else: plt.close()
    
    if toUpload:
        database_folder = os.path.join("GOESimages", product.split("-")[-1][:-1])
        dbu.UploadFile(GeoColorParams["FullImagePath"], database_folder, GeoColorParams["ImageName"])
    
    return fig, ax

def ProductData(FullFilePath, product, n=1):
    isACM, isACHA, isACTP, isACHT, isLST, isRRQPE, isDSR, isDMWV, isTPW = gimp._WhichProduct(product)
    identifier = product.split("-")[-1][:-1]
    
    if isDMWV:
        data_re = xr.open_dataset(FullFilePath, engine='netcdf4')
        data_re.close()
        ProductParams = get_image_params(data_re, identifier)
    else:
        data = xr.open_dataset(FullFilePath, engine='rasterio')
        data.close()
        crs_obj = data.rio.crs
        ProductParams = get_image_params(data, identifier)
        if isACHA or isACTP or isACHT or isLST or isRRQPE or isDSR or isTPW: varname = ProductParams["VarNames"][0]
        elif isACM: varname = ProductParams["VarNames"][1]
        
        data_var = data.isel(band=0)[varname]
        data_re = data_var.rio.reproject(map_proj_pc[0]) # , resolution=0.01
        data_re = data_re.sel(x=slice(PeruLimits_deg[0], PeruLimits_deg[1]), y=slice(PeruLimits_deg[3], PeruLimits_deg[2]))
        data_re = data_re.isel(y=slice(None, None, -1))
        
        if n==0 or n==1:
            print("No interpolation performed")
        else:
            # Interpolation
            x, y = data_re.x.values, data_re.y.values
            xnew, ynew = np.linspace(x[0], x[-1], num=n*len(x)), np.linspace(y[0], y[-1], num=n*len(y))
            if isACHT or isLST: 
                if isLST:
                    for i in range(20):
                        data_re = data_re.interpolate_na(dim="y", method="linear", limit=1, use_coordinate=True)
                        data_re = data_re.interpolate_na(dim="x", method="linear", limit=1, use_coordinate=True)
                else: 
                    data_re = data_re.interpolate_na(dim="x", method="linear", limit=2)
                    data_re = data_re.interpolate_na(dim="y", method="linear", limit=2)
                data_re = data_re.interp(x=xnew, y=ynew)
            else: 
                data_re = data_re.fillna(0).interp(x=xnew, y=ynew)
                data_re = data_re.where(data_re >= 0, other=0)
        
        # Processing
        attributes = data_re.attrs 
        if isACM:
            # mask0 = (data_re.values < 0.5)
            # mask1 = (data_re.values >= 0.5) | (data_re.values < 1.5)
            # mask2 = (data_re.values >= 1.5) | (data_re.values < 2.5)
            # mask3 = (data_re.values >= 2.5)
            # data_re.values[mask0] = 0
            # data_re.values[mask1] = 1
            # data_re.values[mask2] = 2
            # data_re.values[mask3] = 3
            mask = (data_re.values == 0)
            # data_re.values[mask] = np.nan
        elif isACHT or isLST:
            data_re = data_re - 273.15
            data_re.attrs = attributes
            if data_re.units=="K": data_re.attrs["units"] = "°C"
        else: # isACTP or isACHA or isRRQPE
            if isACHA:
                data_re = data_re/1e3
                data_re.attrs = attributes
                if data_re.units=="m": data_re.attrs["units"] = "km"
            if not isACTP:
                mask = (data_re.values == 0)
                data_re.values[mask] = np.nan
    # data_re = data_re.rio.write_crs(map_proj_pc[0])
    return data_re, ProductParams

def ProductPlot(data_re, product, axGeo, ProductParams, toSave=False, toDisplay=False, toUpload=False, title="Peru", dpi=300):
    isACM, isACHA, isACTP, isACHT, isLST, isRRQPE, isDSR, isDMWV, isTPW = gimp._WhichProduct(product)
    
    prod_cmap_dic = definingColormaps(False)[product]
    product_cmap = prod_cmap_dic["cmap"]
    
    axProd = copy.deepcopy(axGeo)
    cbar_fontsize = 10
    if isACM or isACTP:
        flag_values = data_re.flag_values#[1:]
        dflag = np.mean(np.diff(flag_values))/2
        flag_meanings = data_re.flag_meanings.split()#[1:]
        flag_meanings = [flag.replace("_", "\n") for flag in flag_meanings]
        if isACM:
            nbin = len(flag_values)
            product_cmap = product_cmap.discrete(nbin)
        im = axProd.pcolormesh(data_re.x, data_re.y, data_re.values, cmap=product_cmap, vmin=flag_values[0] - dflag, vmax=flag_values[-1] + dflag)
        cbar = plt.colorbar(im,ax=axProd, orientation='horizontal',
                            shrink=0.7, pad=0.01)
        cbar.set_ticks(flag_values)
        cbar.set_ticklabels(flag_meanings)
        # units_latex = re.sub(r'(\w)(-)(\d)', r'\1^{-\3}', data_re.units)
        cbar.set_label(r"{}".format(data_re.long_name), size=cbar_fontsize)
    elif isACHA or isACHT or isLST or isRRQPE or isTPW or isDSR:
        im = axProd.pcolormesh(data_re.x, data_re.y, data_re.values, cmap=product_cmap, vmin=prod_cmap_dic["min"], vmax=prod_cmap_dic["max"])
        if isRRQPE or isTPW or isACHA: cbar_extent = "max"
        else: cbar_extent = "both"
        cbar = plt.colorbar(im,ax=axProd, orientation='horizontal', extend=prod_cmap_dic["cbar_extent"], shrink=0.7, pad=0.01)
        units_latex = re.sub(r'(\w)(-)(\d)', r'\1^{-\3}', data_re.units)
        cbar.set_label(r"{} $({})$".format(data_re.long_name,units_latex), size=cbar_fontsize)
    elif isDMWV:
        axProd.set_extent(PeruLimits_deg)
        # Convert GOES wind speed and direction to u- and v-wind components
        gu, gv = spddir_to_uv(data_re.wind_speed, data_re.wind_direction)
        im = axProd.quiver( # barbs
            data_re.lon.data,
            data_re.lat.data,
            gu.data,
            gv.data,
            data_re.wind_speed,
            **cm_wind().cmap_kwargs,
            # length=5,
            scale=10, scale_units='xy', angles='xy',
            transform=pc
        )
        # axProd.gridlines(draw_labels=False, lw=0.75, color='darkgray', alpha=0.7, ls='--')
        cbar = plt.colorbar(im,ax=axProd, orientation='horizontal', shrink=1, pad=0.01)
        units_latex = re.sub(r'(\w)(-)(\d)', r'\1^{-\3}', data_re.wind_speed.units)
        cbar.set_label(r"{} $({})$".format(data_re.wind_speed.long_name,units_latex), size=cbar_fontsize)
    # cbar.set_label(label="asa",size=12)
    cbar.ax.tick_params(labelsize=cbar_fontsize)
    axProd.set_title(f"{ProductParams['ImageTime_str']}\n{title}", loc="right")
    axProd.set_title(f"{ProductParams['ImageTitle']}", loc='left', fontweight='bold', fontsize=10)
    # axProd.set_title("Peru image from satellite GOES\n {}".format(ProductParams['ImgTime_str']))
    
    if toSave:
        ImagePath = os.path.join(ProductParams["ImagePath"], "Peru")
        if not os.path.exists(ImagePath): os.makedirs(ImagePath)
        FullImagePath = os.path.join(ProductParams["ImagePath"], "Peru", ProductParams["ImageName"])
        axProd.figure.savefig(FullImagePath, dpi=dpi, bbox_inches='tight')
        print("Image {} saved in '{}'".format(ProductParams["ImageName"], ImagePath))
    plt.close()
    figProd = axProd.figure
    
    if toDisplay: display(figProd)
    
    if toUpload:
        # database_folder = os.path.join("GOESimages", product.split("-")[-1][:-1], "Peru")
        dbu.UploadFile(FullImagePath, prod_cmap_dic["type"], ProductParams["ImageName"]) # database_folder
    
    return figProd

def DepartmentPlot(product, dep, RGBdata, GeoColorParams, data_re, ProductParams, toSave=False, toDisplay=False, toUpload=False, dpi=300):
    prod_cmap_dic = definingColormaps(False)[product]
    product_cmap = prod_cmap_dic["cmap"]
    
    if not (product in "ABI-L2-DMWVF"):
        bounding_box = gdf_peru_land[gdf_peru_land["NAME_1"] == dep].geometry.bounds.agg({"minx": "min", "miny": "min", "maxx": "max", "maxy": "max"})
        bounding_box = np.array([bounding_box.minx, bounding_box.maxx, bounding_box.miny, bounding_box.maxy])
        figGeo_dep, axGeo_dep = GeoColorPlot(RGBdata.sel(x=slice(bounding_box[0], bounding_box[1]), y=slice(bounding_box[3], bounding_box[2])), GeoColorParams, department=True, dep=dep, toDisplay=False)
        data_dep = data_re.sel(x=slice(bounding_box[0], bounding_box[1]), y=slice(bounding_box[2], bounding_box[3]))
        figProd_dep = ProductPlot(data_dep, product, axGeo_dep, ProductParams, title=dep+", Peru")

        if toSave:
            DepImagePath = os.path.join(ProductParams["ImagePath"], dep.replace(" ","_"))
            if not os.path.exists(DepImagePath): os.makedirs(DepImagePath)
            DepImageName = ProductParams["ImageName"].split(".")[0] + "_" + dep + ".png"
            DepFullImageName = os.path.join(DepImagePath, DepImageName)
            figProd_dep.savefig(DepFullImageName, dpi=dpi, bbox_inches='tight')
            print("Image {} saved in '{}'".format(DepImageName, DepImagePath))
            
        if toDisplay: display(figProd_dep)
        
        if toSave and toUpload:
            # database_folder = os.path.join("GOESimages", product.split("-")[-1][:-1], dep)
            database_folder = "T"+prod_cmap_dic["type"][-1]+departments_folder[departments.index(dep)]
            database_path = os.path.join("Images",database_folder)
            dbu.UploadFile(DepFullImageName, database_path, DepImageName)


def _ProductReport(data, product):
    if("ACM" in product): # ACM reports
        total_area = np.count_nonzero(~np.isnan(data))
        clear_sky_count = np.count_nonzero((data.values == 0) | (data.values == 1))
        clear_sky_percent = clear_sky_count/total_area*100
        cloudy_sky_count = np.count_nonzero((data.values == 2) | (data.values == 3))
        cloudy_sky_percent = cloudy_sky_count/total_area*100
        
        report = f"{cloudy_sky_percent:.1f}% nublado, {clear_sky_percent:.1f}% despejado"
        # print(report)
    elif("RRQPE" in product): # RRQPE reports
        # Light Rain: 0.1 - 2.0 mm/hour
        # Moderate Rain: 2.1 - 10.0 mm/hour
        # Heavy Rain: 10.1 - 50.0 mm/hour
        # Very Heavy Rain: 50.1 - 100.0 mm/hour
        # Extreme Rain: > 100.0 mm/hour
        mask = np.isnan(data.values)
        data.values[mask] = 0
        total_area = np.count_nonzero(~np.isnan(data))
        thresholds = [0, 0.1, 2.0, 10.0, 50.0, 100.0]
        category_labels = ["Sin lluvia", "Lluvia ligera", "Lluvia moderada", "Lluvia fuerte", "Lluvia muy intensa", "Lluvia extrema"]
        rainfall_categories, intervals = mutl.interval_categorizer(data.values, thresholds, category_labels, lower_endpoint=0)
        
        report = []
        for cat in category_labels[::-1]:
            data_cat = data.where(rainfall_categories[cat]).values
            rain_area = np.count_nonzero(~np.isnan(data_cat))
            rain_area_percent = (rain_area / total_area) * 100
            if rain_area_percent>0: 
                report += [f"{rain_area_percent:.2f}% {cat}"]
    else:
        report = "No output"
    return report

def ReportingEvents(data, product, dep=None, level="L2", send_comments=False):
    reports = ""
    if level=="L1" or level=="L2":
        reports = _ProductReport(data, product)
        print(f"Región del Perú:\n{reports}")
        if send_comments:
            if("ACM" in product): dbu.SendComments("producto_cinco", reports)
            elif("RRQPE" in product): dbu.SendComments("producto_seis", reports)
    if level=="L2":
        for dep in departments:
            print(f"{'='*20} Departamento: {dep} {'='*20}")
            gdf_dep = gdf_peru_land[gdf_peru_land['NAME_1'] == dep]
            polygon_dep = gdf_dep.geometry
            data = data.rio.write_crs(data.goes_imager_projection.crs_wkt)
            data_dep = data.rio.clip(polygon_dep)
            reports = _ProductReport(data_dep, product)
            print(f"Departamento {dep}: {reports}")
            # provinces = gdf_dep["NAME_2"].tolist()
            # if("ACM" in product): # ACM reports
            #     total_area = np.count_nonzero(~np.isnan(data_dep))
            #     clear_sky_count = np.count_nonzero((data_dep.values == 0) | (data_dep.values == 1))
            #     clear_sky_percent = clear_sky_count/total_area*100
            #     cloudy_sky_count = np.count_nonzero((data_dep.values == 2) | (data_dep.values == 3))
            #     cloudy_sky_percent = cloudy_sky_count/total_area*100
            #     
            #     for prov in provinces:
            #         polygon_prov = gdf_dep[gdf_dep['NAME_2'] == prov].geometry
            #         data_prov = data_dep.rio.clip(polygon_prov)
            #         total_area_prov = np.count_nonzero(~np.isnan(data_prov))
            #         cloudy_sky_count = np.count_nonzero((data_prov.values == 2) | (data_prov.values == 3))
            #         cloudy_sky_percent = cloudy_sky_count/total_area_prov*100
            #         print(f"Provincia {prov} {cloudy_sky_percent:.1f}% nublado")
            
                
            #     rain_in = []

            #     for prov in provinces:
            #         polygon_prov = gdf_dep[gdf_dep['NAME_2'] == prov].geometry
            #         data_prov = data_dep.rio.clip(polygon_prov)
            #         there_is_rain = (np.count_nonzero(data_prov.values >= thresholds[1]) > 0)
            #         if there_is_rain: rain_in.append(prov)

            #     if (len(rain_in) > 0):
            #         print(f"Lluvias detectadas en {', '.join(rain_in)}")
            #         for prov in provinces:
            #             polygon_prov = gdf_dep[gdf_dep['NAME_2'] == prov].geometry
            #             data_prov = data_dep.rio.clip(polygon_prov)
            #             rainfall_categories, intervals = interval_categorizer(data_prov.values, thresholds, category_labels, lower_endpoint=0)
            #             print(f"{'-'*10}Provincia: {prov} {'-'*10}")
            #             total_area = np.count_nonzero(~np.isnan(data_prov))
            #             for cat in category_labels[::-1]:
            #                 data = data_prov.where(rainfall_categories[cat]).values
            #                 rain_area = np.count_nonzero(~np.isnan(data))
            #                 rain_area_percent = (rain_area / total_area) * 100
            #                 if rain_area_percent>0: print(f"{cat} {rain_area_percent:.2f}%")
            #     else: print(f"No se detectó lluvia en ninguna provincia de {dep}")
    return reports
    

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

def GettingImagesInfo(ImagesPath, start_date = None, end_date = None, interval = timedelta(days=1)):
    ImagesNames = [img for img in os.listdir(ImagesPath) if img.endswith(".png")]
    ImagesNames.sort()
    df = pd.DataFrame({"Images": ImagesNames,
                   "ImagesFullPath": [os.path.join(ImagesPath, f) for f in ImagesNames]})
    date_format = r"\w+_\w+_(\d{4}_\d{2}_\d{2}_\d{2}_\d{2}).png"  # Define the format of the date in the file names
    df["Time"] = pd.to_datetime(df['Images'].str.extract(date_format, expand=False), format="%Y_%m_%d_%H_%M").dt.tz_localize(utcm5)#.dt.tz_convert(utc)
    df["Product"] = df["Images"].str.extract(r'\w+_([^_]+)_\d{4}_\d{2}_\d{2}_\d{2}_\d{2}.png')
    df = df[["Images", "Time", "Product", "ImagesFullPath"]]
    if not (start_date is None):
        if end_date is None:
            end_date = start_date + interval
        df = df[(df["Time"] >= start_date) & (df["Time"] <= end_date)]
    return df

def GOESvideos(ImagesInfo, VideoPath=".\\", VideoName=None, extension=".mp4", FrameRate = 6):
    
    if VideoName is None:
        product = ImagesInfo["Product"].unique()[0]
        initial_date = ImagesInfo["Time"].iloc[0]
        final_date = ImagesInfo["Time"].iloc[-1]
        unique_days = ImagesInfo["Time"].dt.date.unique()
        if unique_days.size == 1:
            VideoName = product + "_from_" + initial_date.strftime('%H-%M') + "_to_" + final_date.strftime('%H-%M') + "_of_" + unique_days[0].strftime('%d-%b-%y')
        else: 
            VideoName = product + "_from_" + initial_date.strftime('%d-%b-%y') + "_to_"+final_date.strftime('%d-%b-%y')
    
    if not VideoName.endswith(extension):
        VideoName += extension
    
    ImagesList = ImagesInfo["ImagesFullPath"].tolist()
    # if not isinstance(ImagesList, list):
    #     if isinstance(ImagesList, pd.Series):
    #         ImagesList = ImagesList.tolist()
    #     else: 
    #         raise ValueError("ImagesList must be a list or pandas Series.")
    FullVideoName = os.path.join(VideoPath, VideoName)
        
    frame = cv2.imread(ImagesList[0])
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'h264')
    video = cv2.VideoWriter(FullVideoName, fourcc, FrameRate, (width, height))
    for image in ImagesList:
        video.write(cv2.imread(image))
    cv2.destroyAllWindows()
    video.release()

    print(f"Video {VideoName} created successfully in path: '{VideoPath}'")
    
def QueringGeoColorTif(url):
    # Send a GET request to the URL to download the page content
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract text from the <pre> section
        pre_text = soup.find('pre').get_text()
        # Split the text into lines
        lines = pre_text.split('\n')
        # Create a list to hold the data
        data = []
        # Iterate through the lines and split into columns
        for line in lines:
            parts = line.split()
            if len(parts) >= 4:
                filename = parts[-4]
                date = " ".join(parts[-3:-1])
                size = parts[-1]
                data.append([filename, date, int(size)/ (1024 ** 2)])

        # Create a Pandas DataFrame
        df = pd.DataFrame(data, columns=['Filename', 'Date', 'Size'])
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(utc)
        df = df[df["Filename"].str.endswith(".tif")]
    else:
        print("Failed to download the page. HTTP status code:", response.status_code)
    
    return df

# out = {
#             'FileName': data.attrs["dataset_name"],
#             'ImageTitle': ImgTitle,
#             'ImageTime':ImgTime, 'ImageTime_str':ImgTime_str,
#             'VarNames':varnames, 'SpatialResolution': spatial_res,
#             'ImageName': ImageName, 'ImagePath': ImagePath, 'FullImagePath': FullImagePath,
#             'DataAttrs': data.attrs}


def GeoColorTif(destination_path = './GOESimages/', mode="latest"):
    url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/"
    if mode == "latest":
        TifFilesInfo = QueringGeoColorTif(url)
        TifFile = TifFilesInfo.iloc[-1]
        TifFileName = TifFile["Filename"]
        TifFileWebFullPath = os.path.join(url, TifFileName)
        data_tif = rxr.open_rasterio(TifFileWebFullPath)
        data_tif_peru = data_tif.sel(x=slice(PeruLimits_deg[0], PeruLimits_deg[1]), y=slice(PeruLimits_deg[3], PeruLimits_deg[2]))
    
    ImgTime = TifFile["Date"]
    img_year, img_month, img_day = str(ImgTime.year), str(ImgTime.month).zfill(2), str(ImgTime.day).zfill(2)
    img_hour, img_minute = str(ImgTime.hour).zfill(2), str(ImgTime.minute).zfill(2)
    identifier = "GeoColor"
    ImageName = '_'.join([identifier, img_year, img_month, img_day, img_hour, img_minute])+'.png'
    ImagePath = os.path.join(destination_path,'Products',identifier)
    GeoColorParams = dict(FileName = TifFileName, 
                          ImageTime = ImgTime,
                          ImageTime_str = ImgTime.strftime("%d-%b-%Y %H:%M %Z"),
                          ImageName = ImageName, ImagePath = ImagePath)
    
    return data_tif_peru, GeoColorParams




