import os
import urllib.request
import shutil
import zipfile
import tarfile
import lzma
from tqdm import tqdm
import yaml
import subprocess

# Load YAML config
config_path = os.path.join(os.path.dirname(__file__), "config.yml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)
print(yaml.dump(config, sort_keys=False, default_flow_style=True))
dataset_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), config["dataset"]["root_dir"]))
available_datasets = config["dataset"]["available"]
download_datasets = config["dataset"]["download"]
proxy_enabled = config["proxy"]["enabled"]
if proxy_enabled:
    os.environ["HTTP_PROXY"] = config["proxy"]["http"]
    os.environ["HTTPS_PROXY"] = config["proxy"]["https"]
youtube_6m_mirror = config["proxy"]["youtube_6m_mirror"]

def download(url, filename=None):
    if filename is None:
        filename = url.split("/")[-1]
    if os.path.exists(filename):
        print(f"{filename} already exists, skipping download.")
        return
    print(f"Downloading {url} to {filename}...")
    with urllib.request.urlopen(url) as response:
        block_size = 1024 * 1024  # 1MB
        with open(filename, 'wb') as out_file:
            pbar = tqdm(unit='B', unit_scale=True, desc=filename)
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                out_file.write(buffer)
                pbar.update(len(buffer))
            pbar.close()

def extract(filename):
    print(f"Extracting {filename}...")
    if filename.endswith(".tar.gz") or filename.endswith(".tgz"):
        with tarfile.open(filename, "r:gz") as tar:
            tar.extractall()
    elif filename.endswith(".zip"):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall()
    elif filename.endswith(".xz"):
        output_file = filename.replace(".xz", "")
        with lzma.open(filename) as f_in, open(output_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    else:
        raise ValueError(f"Unsupported file type for extraction: {filename}")

def download_and_extract(dataset):
    if dataset not in available_datasets:
        print(f"Dataset '{dataset}' is not available.")
        print(f"Available datasets are: {available_datasets}.")
        exit(1)

    dataset_dir = dataset_root_dir
    parts = dataset.split('-')
    for part in parts:
        dataset_dir = os.path.join(dataset_dir, part)
    os.makedirs(dataset_dir, exist_ok=True)
    os.chdir(dataset_dir)

    if dataset == "sift-1m":
        download("ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz")
        extract("sift.tar.gz")
    elif dataset == "gist-1m":
        download("ftp://ftp.irisa.fr/local/texmex/corpus/gist.tar.gz")
        extract("gist.tar.gz")
    elif dataset == "deep-10m":
        download("https://storage.yandexcloud.net/yandex-research/ann-datasets/DEEP/base.10M.fbin")
        download("https://storage.yandexcloud.net/yandex-research/ann-datasets/DEEP/query.public.10K.fbin")
        download("https://storage.yandexcloud.net/yandex-research/ann-datasets/DEEP/groundtruth.public.10K.ibin")
    elif dataset == "mnist-8m":
        download("https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/mnist8m.xz")
        extract("mnist8m.xz")
        download("https://leon.bottou.org/_media/projects/infimnist.tar.gz")
        extract("infimnist.tar.gz")
        try:
            subprocess.run("cd infimnist && make", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Please run `make` manually in the `infimnist` directory (platform dependent).")
    elif dataset == "mtg-40k":
        download("https://huggingface.co/datasets/TrevorJS/mtg-scryfall-cropped-art-embeddings-open-clip-ViT-SO400M-14-SigLIP-384/resolve/main/README.md", "README.txt")
        for file_number in range(0, 7):
            download(f"https://huggingface.co/datasets/TrevorJS/mtg-scryfall-cropped-art-embeddings-open-clip-ViT-SO400M-14-SigLIP-384/resolve/main/data/train-0000{file_number}-of-00007.parquet")
    elif dataset == "glove-twitter-1m":
        download("https://nlp.stanford.edu/data/glove.twitter.27B.zip")
        extract("glove.twitter.27B.zip")
    elif dataset == "glove-crawl-2m":
        download("https://nlp.stanford.edu/data/glove.42B.300d.zip")
        extract("glove.42B.300d.zip")
    elif dataset == "laion-1m":
        base_url = "https://deploy.laion.ai/8f83b608504d46bb81708ec86e912220"
        for file_number in range(0, 1): # the full laion-500m is range(0,499)
            str_i = str(file_number)
            download(f"{base_url}/embeddings/img_emb/img_emb_{str_i}.npy")
            download(f"{base_url}/embeddings/text_emb/text_emb_{str_i}.npy")
            download(f"{base_url}/embeddings/metadata/metadata_{str_i}.parquet")
    elif dataset == "youtube-6m":
        download("https://research.google.com/youtube8m/csv/2/vocabulary.csv")
        download("http://data.yt8m.org/download.py")
        try:
            partitions = ["2/video/train", "2/video/validate", "2/video/test"]
            # It can be restarted if the connection drops. In which case, it only downloads shards that haven't been downloaded yet. 
            for _ in range(234):
                for partition in partitions:
                    env = os.environ.copy()
                    env["partition"] = partition
                    env["mirror"] = youtube_6m_mirror
                    subprocess.run(["python", "download.py"], check=True, env=env, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print("Please run `python download.py` manually for dataset shards (platform dependent).")

for dataset in download_datasets:
    download_and_extract(dataset)
print("Done!")
