import os
import datetime
import tempfile
import warnings
import shutil
from multiprocessing import Pool
import requests
import urllib3
import drms
import pickle
from aiapy.calibrate.util import get_correction_table, get_pointing_table
import aiapy.psf
import astropy.units as u


def download_url(source, destination):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temporary = f.name
    
    if os.path.exists(destination):
        return False
    try:
        if not os.path.exists(os.path.dirname(destination)):
            os.makedirs(os.path.dirname(destination))
        # 스트리밍을 사용하여 파일 다운로드
        with requests.get(source, stream=True) as response:
            response.raise_for_status()
            with open(temporary, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        # 임시 파일을 최종 목적지로 이동
        shutil.move(temporary, destination)
        os.system(f"chmod 777 {destination}")
        print(f"{source} -> {destination}")
        return True

    except requests.HTTPError as e:
        print(f"{source} : {e}")
        return False
    except requests.RequestException as e:
        print(f"요청 중 오류가 발생했습니다: {e}")
        return False


def get_client(email):
    client = drms.Client(email=email)
    return client
    

def request(client, dt_start):
    dt_end = dt_start + datetime.timedelta(minutes=1)    
    str_start = dt_start.strftime("%Y.%m.%d_%H:%M:%S_TAI")
    str_end = dt_end.strftime("%Y.%m.%d_%H:%M:%S_TAI")
    query_str = f"aia.lev1_euv_12s[{str_start}-{str_end}]"
    print(query_str)
    export_request = client.export(query_str, method='url', protocol='fits')
    export_request.wait()
    return export_request


def download(export_request, out_dir):
    done = False
    source_and_destination = []

    for url in export_request.urls.url:
        filename = os.path.basename(url)
        destination = os.path.join(out_dir, filename)
        source_and_destination.append((url, destination))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        os.system(f"chmod 777 {out_dir}")

    while done is False:
        with Pool(8) as p:
            p.starmap(download_url, source_and_destination)
        not_downloaded = []
        for source, destination in source_and_destination:
            if not os.path.exists(destination):
                not_downloaded.append((source, destination))
        if len(not_downloaded) == 0:
            done = True
        else:
            source_and_destination = not_downloaded


def save_correction_table(file_path):
    correction_table = get_correction_table()
    with open(file_path, 'wb') as f:
        pickle.dump(correction_table, f)


def save_pointing_table(file_path):
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()
    pointing_table = get_pointing_table(start, end)
    with open(file_path, 'wb') as f:
        pickle.dump(pointing_table, f)


def save_psfs(file_path):
    waves = [94, 131, 171, 193, 211, 304, 335]
    psfs = {}
    for wave in waves:
        psf = aiapy.psf.psf(wave*u.angstrom)
        psfs[str(int(wave))] = psf
    with open(file_path, 'wb') as f:
        pickle.dump(psfs, f)
