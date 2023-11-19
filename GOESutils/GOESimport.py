import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pytz, re
import xarray as xr
import cartopy.crs as ccrs
map_proj_pc = ccrs.PlateCarree(), "PlateCarree projection"
PeruLimits_deg = [-85, -67.5, -20.5, 1.0] # Peru boundary coordinates
utc = pytz.timezone('UTC') # UTC timezone
utcm5 = pytz.timezone('America/Lima') # UTC-5 timezone
from IPython.display import display, Image, clear_output
import os, time, requests
import GOESutils.MyUtils as mutl
import s3fs
fs = s3fs.S3FileSystem(anon=True)

import keyboard
from IPython.display import display
destination_path = './GOESimages/'

# Define parameter options and aliases
# ------------------------------------
_satellite = {
    "noaa-goes16": [16, "16", "G16", "EAST", "GOES16"],
    "noaa-goes17": [17, "17", "G17", "WEST", "GOES17"],
    "noaa-goes18": [18, "18", "G18", "WEST", "GOES18"],
}
_domain = {
    "C": ["CONUS"],
    "F": ["FULL", "FULLDISK", "FULL DISK"],
    "M": ["MESOSCALE", "M1", "M2"],
}

def GOESdownload(df, local_path, overwrite=False, verbose=True):
    while not mutl.check_internet_connection():
        print("Waiting for internet connection.")
        time.sleep(30)
    print(f"Downloading products: {', '.join(df['product'].unique().tolist())} (Press 'esc' to stop)")
    for file, date in zip(df.file, df.creation):
        filepath = os.path.dirname(file)
        filename = os.path.basename(file)
        if local_path is None:
            file_localpath = os.path.join(destination_path,filepath)
        else:
            file_localpath = destination_path
        local_file = os.path.join(file_localpath, filename)
        if not os.path.exists(file_localpath):
            os.makedirs(file_localpath)
        msg = ""
        if os.path.exists(local_file) and not overwrite: 
            msg = f"\rFile [{filename}] already exists on [{file_localpath}]. Do not overwrite"
        else:
            msg = f"\rDownloading file {filename} created on {date.strftime('%d-%b-%Y %H:%M %Z')}"
            fs.get(file, local_file)
        print(msg, end='', flush=True)
        if keyboard.is_pressed("esc"): 
            print("\rThe 'esc' key was pressed. Exit request gotten.")
            exit_request = True
            break
        # clear_output(wait=True)
    print(f"\rFinished downloading {len(df)} files to [{destination_path}]".ljust(2*len(msg)))
    

def GOESfiles(mode="timerange", 
              startdate=None, 
              enddate=None, freq=None, 
              satellite="noaa-goes16", instrument="ABI", domain="F", target_product="ABI-L2-MCMIPF", bands=None, 
              download=False, overwrite=False, local_path=None,
              to_display=False):
    """
    Get list of requested GOES files as pandas.DataFrame.
        Products available on:
        https://github.com/awslabs/open-data-docs/tree/main/docs/noaa/noaa-goes16
        
        Parameters
        ----------
        freq: str, int, pd.DateOffset, or function
            The resampling rule, which determines the frequency of resampling. Accepted values include:
            - String representations for common time frequencies:
            - 'D': Daily frequency.
            - 'B': Business day frequency (excludes weekends).
            - 'W': Weekly frequency.
            - 'M': Month end frequency.
            - 'Q': Quarter end frequency.
            - 'A': Year end frequency.
            - Custom frequency strings like '2H' for every 2 hours, '3T' for every 3 minutes, '10S' for every 10 seconds, and so on.
            - Offset aliases like 'B' (business day), 'W-MON' (weekly anchored to Mondays), 'M-2' (every 2 months), 'Q-DEC' (quarterly anchored to December), 'A-JAN' (annual anchored to January), etc.
            - Date offset objects like pd.DateOffset(days=1) for a custom day frequency or pd.DateOffset(hours=2) for a 2-hour frequency.
            - Timedelta objects, such as pd.Timedelta(days=7) for a 7-day frequency or pd.Timedelta(minutes=15) for a 15-minute frequency.
            - Integers for rolling windows using integers, like 3, to create rolling windows of a fixed size.
            - Custom resampling defined functions and pass them as the 'rule' parameter. The function should take a DataFrame as input and return a resampled DataFrame.
            
            
        Example:
        startdate = datetime(2020,1,1,1,tzinfo=utcm5)
        enddate = datetime(2020,1,1,2,tzinfo=utcm5)
        target_product = "RadF"
        bands = [1, 5]
    """
    
    if startdate is None: startdate = datetime.now(utcm5)-timedelta(hours=1)
    if enddate is None: enddate = datetime.now(utcm5)
    startdate = startdate.astimezone(utc)
    enddate = enddate.astimezone(utc)
    if not isinstance(target_product, list): target_product = [target_product]
    
    # (Satellite and Domain validation from goes2go.data._check_param_inputs)
    ## Determine the Satellite 
    if satellite not in _satellite:
        satellite = str(satellite).upper()
        for key, aliases in _satellite.items():
            if satellite in aliases:
                satellite = key
    assert (
        satellite in _satellite
    ), f"satellite must be one of {list(_satellite.keys())} or an alias {list(_satellite.values())}"
    ## Determine the Domain (only needed for ABI product)
    for i_p, product in enumerate(target_product):
        if product[-1] in _domain:
            # If the product has the domain, this takes priority
            domain = product[-1]
        elif isinstance(domain, str):
            domain = domain.upper()
            if domain in ["M1", "M2"]:
                target_product[i_p] = product + "M"
            else:
                for key, aliases in _domain.items():
                    if domain in aliases:
                        domain = key
                target_product[i_p] = product + domain
        assert (domain in _domain) or (
            domain in ["M1", "M2"]
        ), f"domain must be one of {list(_domain.keys())} or an alias {list(_domain.values())}"
    #
    
    if bands is None:
        bands = []
        for i in range(17):
            bands.append(f"{i:02d}")
        bands
    if not isinstance(bands, list): bands = [bands]
    params = locals()
    bucket_content = list(map(lambda x: x.split("/")[-1], fs.ls(f"s3://{satellite}/", refresh=True)))
    products = [s for s in bucket_content if s.startswith(instrument)]
    matching_products = []
    for product in target_product:
        matching_products += [next((p for p in products if product in p), None)]
    band_mapping = {}
    for i in range(1, 17):
        band_mapping[i] = f"{i:02d}"
    band_strings = [band_mapping.get(band, band) for band in bands]
    file_sizes, files = [], []
    exit_request = False
    print(f"Searching for products: {', '.join(matching_products)} (Press 'esc' to stop)")
    for product in matching_products:
        dates = pd.date_range(f"{startdate:%Y-%m-%d %H:00}", f"{enddate:%Y-%m-%d %H:00}", freq="1H")         
        for date in dates:
            try:
                print(f"\rLooking for product {product}, set of files from date {date.strftime('%d-%b-%Y %H:%M %Z')}", end='', flush=True)
                detailed_files = fs.ls(f"{satellite}/{product}/{date:%Y/%j/%H/}", refresh=True, detail=True)
            except FileNotFoundError:
                date = date - timedelta(minutes=10)
                print(f"\rLooking for product {product}, set of files from date {date.strftime('%d-%b-%Y %H:%M %Z')}", end='', flush=True)
                detailed_files = fs.ls(f"{satellite}/{product}/{date:%Y/%j/%H/}", refresh=True, detail=True)
            for f in detailed_files:
                files += [f["name"]]
                file_sizes += [f["size"]]
            if keyboard.is_pressed("esc"): 
                print("The 'esc' key was pressed. Exit request gotten.")
                exit_request = True
                break
        if exit_request:
            break
    print("")
    df = pd.DataFrame({"file": files})
    df['start'] = pd.to_datetime(df["file"].str.extract(r'_s(\d{13})')[0], format='%Y%j%H%M%S').dt.tz_localize(utc).dt.tz_convert(utcm5)#.dt.strftime("%d-%b-%Y %H:%M UTC%Z")
    df['end'] = pd.to_datetime(df["file"].str.extract(r'_e(\d{13})')[0], format='%Y%j%H%M%S').dt.tz_localize(utc).dt.tz_convert(utcm5)#.dt.strftime("%d-%b-%Y %H:%M UTC%Z")
    df['creation'] = pd.to_datetime(df["file"].str.extract(r'_c(\d{13})')[0], format='%Y%j%H%M%S').dt.tz_localize(utc).dt.tz_convert(utcm5)#.dt.strftime("%d-%b-%Y %H:%M UTC%Z")
    
    pattern = r"ABI-(L1b|L2)-([A-Za-z]+)"
    df['product'] = df["file"].apply(lambda x: re.search(pattern, os.path.basename(x)).group(0) if re.search(pattern, os.path.basename(x)) else None)
    band_pattern = r"-M\dC(\d+)_"
    df['band'] = df['file'].str.extract(band_pattern)#.astype(int, errors='ignore')
    df.band.fillna("None", inplace=True)
    # df['size'] = df["file"].apply(lambda x: f"{os.path.getsize(x)/1024**2:.2f} MB")
    df['size'] = file_sizes
    df['size'] = df['size'].apply(lambda x: f"{x/1024**2:.2f} MB")
    df = df.loc[df.creation >= startdate].loc[df.creation <= enddate]
    band_strings.append("None")
    if any("Rad" in s for s in matching_products):
        df = df.loc[df.band.isin(band_strings)]
    if mode=="latest":
        df = df.sort_values(by='file', ascending=True).groupby(["product", "band"]).tail(1)
    df.reset_index(drop=True, inplace=True)
    if freq is not None:
        df = (df.groupby(["product", "band"])
                .resample(freq, on='creation', origin='start').first()
                .reset_index(level=["band", "product"], drop=True)
                .reset_index())
    df = df[["file","start","end","creation","product","band","size"]]
    total_size_bytes = df['size'].str.extract(r'([\d.]+)').astype(float).sum(skipna=True)[0]*1024**2
    total_size, size_units = mutl.format_file_size(total_size_bytes)
    if download: # Downloading files requested
        GOESdownload(df, local_path, overwrite)
    print(f"Total Size: {total_size:.2f} {size_units}")
    if to_display: display(df)
    
    for i in params:
        df.attrs[i] = params[i]
    return df

def GetDataParameters(data, product, image_path='./GOESimages/'):
    ImgTitle = data.attrs['title'].split("ABI L2 ")[-1]
    ImgTitle = ImgTitle.split(" - ")[0]
    format_string = '%Y-%m-%dT%H:%M:%S.%fZ'
    time_coverage_start = datetime.strptime(data.attrs['time_coverage_start'], format_string)
    time_coverage_end = datetime.strptime(data.attrs['time_coverage_end'], format_string)
    ImgTime = time_coverage_end
    # ImgTime = time_coverage_start + (time_coverage_end - time_coverage_start) / 2
    ImgTime = ImgTime.replace(tzinfo = utc)
    ImgTime = ImgTime.astimezone(utcm5)
    ImgTime_str = ImgTime.strftime('%d/%m/%Y %H:%M UTC%Z') # '%H:%M UTC %d-%b-%Y'
    varnames = list(data.data_vars.keys())
    spatial_res = data.attrs["spatial_resolution"].split()[0]
    # spatial_res = float(re.findall('\d+',spatial_res)[0])
    # Building image name format
    img_year, img_month, img_day = str(ImgTime.year), str(ImgTime.month).zfill(2), str(ImgTime.day).zfill(2)
    img_hour, img_minute = str(ImgTime.hour).zfill(2), str(ImgTime.minute).zfill(2)
    satellite = data.attrs["platform_ID"]
    ImageName = '_'.join([satellite, product, img_year, img_month, img_day, img_hour, img_minute])+'.png'
    ImagePath = os.path.join(image_path,'Products', product)
    FullImageName = os.path.join(ImagePath,ImageName)
    ImageParameters = {
            'FileName': data.attrs["dataset_name"],
            'ImageTitle': ImgTitle,
            'ImageTime':ImgTime, 'ImageTime_str':ImgTime_str,
            'VarNames':varnames, 'SpatialResolution': spatial_res,
            'ImageName': ImageName, 'ImagePath': ImagePath, 'FullImageName': FullImageName,
            'DataAttrs': data.attrs}
    return ImageParameters

def _WhichProduct(product):
    # global isACM, isACHA, isACTP, isACHT, isLST, isRRQPE, isDSR, isDMWV, isTPW
    isACM = isACHA = isACTP = isACHT = isLST = isRRQPE = isDSR = isDMWV = isTPW = False
    if bool(re.search(product, "ABI-L2-ACMF")): isACM = True
    elif bool(re.search(product, "ABI-L2-ACHAF")): isACHA = True
    elif bool(re.search(product, "ABI-L2-ACTPF")): isACTP = True
    elif bool(re.search(product, "ABI-L2-ACHTF")): isACHT = True
    elif bool(re.search(product, "ABI-L2-LSTF")): isLST = True
    elif bool(re.search(product, "ABI-L2-RRQPEF")): isRRQPE = True 
    elif bool(re.search(product, "ABI-L2-DSRF")): isDSR = True
    elif bool(re.search(product, "ABI-L2-DMWVF")): isDMWV = True
    elif bool(re.search(product, "ABI-L2-TPWF")): isTPW = True
    return isACM, isACHA, isACTP, isACHT, isLST, isRRQPE, isDSR, isDMWV, isTPW

def ImportingData(file, product):
    isACM, isACHA, isACTP, isACHT, isLST, isRRQPE, isDSR, isDMWV, isTPW = _WhichProduct(product)
    identifier = product.split("-")[-1][:-1]
    
    if isDMWV:
        data_re = xr.open_dataset(file, engine='netcdf4')
        data_re.close()
        ProductParams = GetDataParameters(data_re, identifier)
    else:
        data = xr.open_dataset(file, engine='rasterio')
        data.close()
        crs_obj = data.rio.crs
        ProductParams = GetDataParameters(data, identifier)
        if isACHA or isACTP or isACHT or isLST or isRRQPE or isDSR or isTPW: varname = ProductParams["VarNames"][0]
        elif isACM: varname = ProductParams["VarNames"][1]
        else: varname = ProductParams["VarNames"][0]
        
        data_var = data.isel(band=0)[varname]
        data_re = data_var.rio.reproject(map_proj_pc[0]) # , resolution=0.01
        data_re = data_re.isel(y=slice(None, None, -1))
        data_re = data_re.sel(x=slice(PeruLimits_deg[0], PeruLimits_deg[1]), y=slice(PeruLimits_deg[2], PeruLimits_deg[3]))
    return data_re, ProductParams

def CleaningData(data, product):
    isACM, isACHA, isACTP, isACHT, isLST, isRRQPE, isDSR, isDMWV, isTPW = _WhichProduct(product)
    # Processing
    attributes = data.attrs 
    if isACM:
        # mask0 = (data_re.values < 0.5)
        # mask1 = (data_re.values >= 0.5) | (data_re.values < 1.5)
        # mask2 = (data_re.values >= 1.5) | (data_re.values < 2.5)
        # mask3 = (data_re.values >= 2.5)
        # data_re.values[mask0] = 0
        # data_re.values[mask1] = 1
        # data_re.values[mask2] = 2
        # data_re.values[mask3] = 3
        mask = (data.values == 0)
        # data_re.values[mask] = np.nan
    elif isACHT or isLST:
        data = data - 273.15
        data.attrs = attributes
        if data.units=="K": data.attrs["units"] = "°C"
    elif isACHA:
        data = data/1e3
        data.attrs = attributes
        if data.units=="m": data.attrs["units"] = "km"
    else: # isACTP or isACHA or isRRQPE
        if not isACTP:
            mask = (data.values == 0)
            data.values[mask] = np.nan
    return data

def GeoColorData(file):
    gdata = xr.open_dataset(file, engine='rasterio').isel(band=0)

    crs_obj = gdata.rio.crs
    crs_dest = map_proj_pc[0] # "EPSG:4326"
    GeoColorParams = GetDataParameters(gdata, "RGB", image_path='./GOESimages/')
    print(f"Reading file {GeoColorParams['FileName']} as geocolor image.")
    ImageTime = GeoColorParams['ImageTime']
    isDay = (ImageTime.hour>5 and ImageTime.hour<17)
    if isDay: GeoColor = gdata.rgb.NaturalColor(night_IR=False).rio.write_crs(crs_obj)
    else: GeoColor = gdata.rgb.TrueColor(night_IR=True).rio.write_crs(crs_obj)
        
    R, G, B = [
        GeoColor.isel(rgb=i).rio.reproject(crs_dest) # , resolution=0.01
        .sel(x=slice(PeruLimits_deg[0], PeruLimits_deg[1]), y=slice(PeruLimits_deg[3], PeruLimits_deg[2]))
        for i in range(3)
    ]
    RGBdata = xr.concat([R, G, B], dim='rgb').transpose('y', 'x', 'rgb')
    return RGBdata, GeoColorParams



# old_files = os.listdir(ImgPath)
        # old_png_files = set([file for file in old_files if file.endswith('.png')])
        # are_there_old_filenames = (len(old_png_files) > 0)