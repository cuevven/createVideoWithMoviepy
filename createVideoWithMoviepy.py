# -*- coding: utf-8 -*-
print('>>>>>>>>>>>>>>开始加载库>>>>>>>>>>>>>>')
import os
import math
import librosa
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ImageSequenceClip, ImageClip
import moviepy.video.fx.all as vfx
import click
from utils import resizeImage, readDir


"""
对于默认的 16:9 宽高比，请按以下分辨率进行编码：
2160p：3840x2160
1440p：2560x1440
1080p：1920x1080 30fps/60fps 4000k-6000k/6000k-9000k
720p：1280x720
480p：854x480
360p：640x360
240p：426x240

:param width: 生成视频的宽度 default: 1920 
:param height: 生成视频的高度 default: 1080
:param images_origin: 源图片的路径
:param origin_target_dir: 将源路径替换为目标路径。
    这个项目的源路径是爬虫下载图片的路径，最后还要把下载的图片处理成和视频一样的大小存放在目标目录
    default: ('./src/images', './src/imgs')
:param music: 背景音乐路径
:param fps: 视频的帧率 default: 30
:param output: 生成视频的文件名
"""


@click.command()
@click.option('--width', prompt='Width', default=1920, help='The width of video clips')
@click.option('--height', prompt='Height', default=1080, help='The height of video clips')
@click.option('--images_origin', prompt='images file', default='./src/images', help='The source images path')
@click.option('--origin_target_dir', prompt='replace origin dir to target dir', default=('./src/images', './src/imgs'), help='how replace origin dir to target dir')
@click.option('--music', prompt='Music file', default='./src/music/1302.mp3', help='The music file')
@click.option('--fps', prompt='video fps ', default=30, help='The output video fps')
@click.option('--output', prompt='Output file', default='./dist/1353112775.mp4', help='The output file name')
def main(width, height, images_origin, origin_target_dir, music, fps, output):
    target_images_dir = images_origin.replace(origin_target_dir[0], origin_target_dir[-1])
    if not os.path.exists(target_images_dir):
        filesPath = readDir(images_origin)
        print('>>已载入文件 %s 个' % len(filesPath))
        print('>>>>>>>>>>>>>>开始调整图片大小>>>>>>>>>>>>>>')
        for img in filesPath:
            resizeImage(img, origin_target_dir, (width, height))

    print('>>>>>>>>>>>>>>开始读取调整过的图片>>>>>>>>>>>>>>')
    filesPath = readDir(images_origin.replace(origin_target_dir[0], origin_target_dir[-1]))
    print('>>已载入文件 %s 个' % len(filesPath))

    print('>>>>>>>>>>>>>>开始分析节拍>>>>>>>>>>>>>>')
    y, sr = librosa.load(music, sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = list(librosa.frames_to_time(beats, sr=sr))
    beat_times.append(beat_times[-1] + 1)


    clips = []
    audio_time = librosa.get_duration(filename=music)
    print('>>音频时长(s):%f >>节拍数量：%s' % (audio_time, len(beat_times)))
    interval = math.ceil(abs( len(beat_times) / len(filesPath) ))
    filesPath = [f for f in filesPath for i in range( interval )]
    print('>>新的文件列表长度:%s' % len(filesPath))

    print('>>>>>>>>>>>>>>开始按节拍生成视频帧>>>>>>>>>>>>>>')
    for index, beat_time in enumerate(beat_times[:-1]):
        if index >= len( filesPath):
            print('>>图片数量不足以匹配节拍，中止匹配。输出的视频后段可能会出现黑屏。')
            print('>>图片数量：{0} >节拍数量：{1}'.format(len( filesPath), len(beat_times)))
            break
        print(f'{index + 1}/{len(beat_times)}>>{ filesPath[index]}')
        time_diff = math.modf(beat_time - beat_times[index -1])
        time_diff = math.ceil(time_diff[0]*10) if (time_diff[0] * 10) > time_diff[-1] else math.ceil(time_diff[-1])
        image_clip = (ImageClip(filesPath[index], duration=abs(time_diff)*fps)
                    .set_fps(abs(time_diff)*fps)
                    .set_start(beat_time)
                    .set_end(beat_times[index + 1]))
        image_clip = image_clip.set_pos('center')
        if index % interval == 0:
            image_clip = image_clip.fx(vfx.fadein, duration=0.5)
        clips.append(image_clip)


    print('>>>>>>>>>>>>>>开始合并剪辑，生成视频>>>>>>>>>>>>>>')
    final_clip = CompositeVideoClip(clips)
    audio_clip = AudioFileClip(music)
    final_video = final_clip.set_audio(audio_clip)
    final_video.write_videofile(
        output,
        fps=fps,
        codec='mpeg4',
        # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo
        preset='medium',
        audio_codec="libmp3lame",
        threads=4,
        bitrate ='6000k')


if __name__ == '__main__':
    main()
