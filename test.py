import os
import shutil
import sys
from huggingface_hub import snapshot_download
cache_dir = "./capu"
def download_files(repo_id, cache_dir=None, ignore_regex=None):
    download_dir = snapshot_download(repo_id=repo_id, cache_dir=cache_dir)
    if cache_dir is None or download_dir == cache_dir:
        return download_dir
    file_names = os.listdir(download_dir)
    for file_name in file_names:
        shutil.move(os.path.join(download_dir, file_name), cache_dir)
    os.rmdir(download_dir)
    return cache_dir
cache_dir = download_files(repo_id="dragonSwing/xlm-roberta-capu", cache_dir=cache_dir)
sys.path.append(cache_dir)
