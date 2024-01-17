# detect_blur

Quick diry method to detect if an image is blurry or not.

## Usage

Clone the [repository](https://github.com/ChrCoello/detect_blur.git) from GitHub
```shell
git clone https://github.com/ChrCoello/detect_blur.git
```

Install the necessary dependencies using poetry. It will create a virtual environement for this project.
```shell
cd detect_blur
poetry install
```

Test using the list of urls in the json file under assets
```shell
poetry shell 
python src/main.py -j assets/list_images.json
```