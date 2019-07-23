# [create video with Moviepy](https://github.com/cuevven/createVideoWithMoviepy)

用 moviepy 把图片生成视频。[代码的分析在这里](https://cuevven.github.io/Technology/Python/create-video-with-moviepy/)

## :star: 特性

- 使用 python 3.7
- moviepy
- librosa

## :rocket: 使用者指南

```bash
git clone https://github.com/cuevven/createVideoWithMoviepy.git

cd createVideoWithMoviepy

python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

python createVideoWithMoviepy.py
```

## :bulb: 需要注意的事情

- `./src/music`目录，需要你自己扔首`.mp3`进去，然后在参数中指定路径；
- 你需要自己创建 `./src/images` 这个目录，并且把原始图片放在里面；
