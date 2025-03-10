import json
import os
import subprocess
from manim import *



class Template(Scene):
    # 初始化代码
    def __init__(self):
        super().__init__()
        # 初始化总时间计数器、字幕文件、字幕编号、字幕字体大小、单字符语音时间
        self.default_output_dir = 'media'
        self.animation_timer = 0.0
        self.subtitle_id = 0
        self.subtitle_font_size = 28
        self.time_per_char = 0.3

        # 确保缓存目录存在
        os.makedirs(self.default_output_dir, exist_ok=True)
        self.subtitle_file = os.path.join(self.default_output_dir, "subtitles.jsonl")

        # 如果字幕文件存在，则清空文件，否则创建文件
        if os.path.exists(self.subtitle_file):
            with open(self.subtitle_file, 'w', encoding='utf-8') as f:
                f.write('')  # 写入空字符串，即清空文件
            print(f"已清空字幕文件: {self.subtitle_file}")
        else:
            os.makedirs(os.path.dirname(self.subtitle_file), exist_ok=True)
        
        # 初始化字幕对象
        self.subtitle = Text("", font_size=self.subtitle_font_size) 
    
    # 用于构建字幕并自动计时的函数
    def update_subtitle(self, text, wait=0.0, fontsize=24):
        """更新字幕并同步写入字幕文件，包括时间。注意需要内置动画计时器支持"""
        # 如果有旧字幕，先移除
        if hasattr(self, 'subtitle') and self.subtitle is not None:
            self.remove(self.subtitle)
        
        # 如果文本不为空，则创建新字幕
        if text:
            new_subtitle = Text(text, font_size=fontsize)
            new_subtitle.to_edge(DOWN)

            # 将字幕添加到场景中
            # self.add_fixed_in_frame_mobjects(new_subtitle) # 3D 模式下用这个
            self.add(new_subtitle) # 2D 模式下用这个
            self.subtitle = new_subtitle

            # 将字幕记录到 jsonl 文件，包括编号、开始时间、文本内容
            self.subtitle_id += 1
            subtitle_json = {
                "id":           self.subtitle_id, 
                "text":         text.strip(),  # 移除空白
                "start_time":   self.animation_timer
                }
            with open(self.subtitle_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(subtitle_json, ensure_ascii=False) + '\n')

        # 默认情况下根据字符数目自动决定等待时间
        if wait==0:
            wait = len(text) * self.time_per_char
        else:
            wait = wait
            
        # 等待语音播放并更新动画计时器
        self.wait(wait); self.animation_timer += float(wait)
    
    # 构建动画的主体
    def construct(self):
        
        # 播放字幕时可以明确设定 wait 参数，不设定的话会根据字符数和 self.time_per_char 自动决定等待时间
        self.update_subtitle("这里是基于 manim 的动画模板")
        self.update_subtitle("首先让我们创建一个复平面作为展示")

        # 创建复平面
        complex_plane = ComplexPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.6
            },
            axis_config={
                "include_tip": True,  # 添加箭头
                "include_numbers": True,  # 添加数字标签
                "include_ticks": True,  # 添加刻度
                "tip_shape": ArrowTriangleFilledTip  # 箭头形状
            },
            x_axis_config={"label_direction": DOWN},  # x轴标签方向
            y_axis_config={"label_direction": LEFT}   # y轴标签方向
        ).scale(1.0)
        
        # 添加坐标轴标签
        x_label = MathTex("Re(z)").next_to(complex_plane.x_axis, RIGHT, buff=0.3)
        y_label = MathTex("Im(z)").next_to(complex_plane.y_axis, UP, buff=0.3)
        complex_plane.add(x_label, y_label)
        
        # 播放任何动画动作时必须设置 run_time 参数并维护动画计时器 animation_timer
        # 这样才能确保字幕与动画同步，于是可以自动生成字幕语音。
        self.play(Create(complex_plane), run_time=2.0)
        self.animation_timer += 2.0

        # ------------------------------
        # 在这里添加任何动画
        # ------------------------------

        self.update_subtitle("模板就到这里。", wait=3)




# 主函数
if __name__ == "__main__":
    # 定义 manim 命令行参数
    quality = "l"  # 可选的有 l, m, h, k
    preview = ""   # 不自动预览，若需要预览可设为 "-p"
    
    quality_to_str = {
        "l": "480p15",
        "m": "720p30",
        "h": "1080p60",
        "k": "2160p60"
    }; quality_str = quality_to_str.get(quality)

    # 构建并执行 manim 命令，-q 指定渲染质量，-p 指定预览，__file__ 指定当前文件，Template 指定类名
    cmd = f"manim -q{quality} {preview} {__file__} Template"
    result = subprocess.run(cmd, shell=True)

    from generate_speech import generate_speech
    # 根据 manim 的输出结构确定文件路径
    # 视频文件路径：media/videos/template/质量标识/类名.mp4
    # 字幕文件路径：media/subtitles.jsonl
    video_file = f"media/videos/template/{quality_str}/Template.mp4"
    subtitles_file = "media/subtitles.jsonl"
    
    # 调用语音生成函数，使用阿里云的龙老铁音色，因其断句一般较好
    generate_speech(video_file, subtitles_file, 'longlaotie')
    
    print(f"动画已通过命令行渲染完成，带配音的文件为：{video_file.replace('.mp4', '_WithAudio.mp4')}")