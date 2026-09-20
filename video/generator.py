import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

from video.scenes import Scene


WIDTH = 1080
HEIGHT = 1920
FPS = 30


class VideoGenerator:

    def __init__(self, output_dir="data/videos"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_font(self, size):

        fonts = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/verdana.ttf",
        ]

        for font in fonts:

            if os.path.exists(font):
                return ImageFont.truetype(
                    font,
                    size
                )

        return ImageFont.load_default()

    def _create_frame(
        self,
        scene,
        frame_number,
        total_frames
    ):

        image = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            scene.background
        )

        draw = ImageDraw.Draw(image)

        progress = (
            frame_number
            / max(total_frames - 1, 1)
        )

        glow_x = int(
            WIDTH * (
                0.2 +
                0.6 * progress
            )
        )

        glow_y = HEIGHT // 2

        draw.ellipse(
            (
                glow_x - 250,
                glow_y - 250,
                glow_x + 250,
                glow_y + 250
            ),
            fill=(
                min(
                    scene.background[0] + 25,
                    255
                ),
                min(
                    scene.background[1] + 25,
                    255
                ),
                min(
                    scene.background[2] + 25,
                    255
                )
            )
        )

        font = self._get_font(
            scene.font_size
        )

        max_width = WIDTH - 160

        words = scene.text.split()

        lines = []
        current_line = ""

        for word in words:

            candidate = (
                current_line + " " + word
                if current_line
                else word
            )

            bbox = draw.textbbox(
                (0, 0),
                candidate,
                font=font
            )

            if bbox[2] - bbox[0] <= max_width:

                current_line = candidate

            else:

                if current_line:
                    lines.append(
                        current_line
                    )

                current_line = word

        if current_line:
            lines.append(
                current_line
            )

        line_height = (
            scene.font_size * 1.25
        )

        total_height = (
            len(lines) * line_height
        )

        y = (
            HEIGHT / 2
            - total_height / 2
        )

        animation = min(
            progress * 5,
            1
        )

        offset = int(
            (1 - animation) * 100
        )

        y += offset

        for line in lines:

            bbox = draw.textbbox(
                (0, 0),
                line,
                font=font
            )

            text_width = (
                bbox[2] - bbox[0]
            )

            x = (
                WIDTH - text_width
            ) / 2

            draw.text(
                (
                    x + 6,
                    y + 6
                ),
                line,
                font=font,
                fill=(0, 0, 0)
            )

            draw.text(
                (
                    x,
                    y
                ),
                line,
                font=font,
                fill=(255, 255, 255)
            )

            y += line_height

        bar_x = 60
        bar_y = HEIGHT - 100
        bar_width = WIDTH - 120
        bar_height = 12

        draw.rounded_rectangle(
            (
                bar_x,
                bar_y,
                bar_x + bar_width,
                bar_y + bar_height
            ),
            radius=6,
            fill=(60, 60, 60)
        )

        draw.rounded_rectangle(
            (
                bar_x,
                bar_y,
                bar_x + int(
                    bar_width * progress
                ),
                bar_y + bar_height
            ),
            radius=6,
            fill=(255, 255, 255)
        )

        return image

    def _render_scene(
        self,
        scene,
        output_path
    ):

        frame_count = max(
            1,
            int(scene.duration * FPS)
        )

        with tempfile.TemporaryDirectory() as temp:

            frame_pattern = os.path.join(
                temp,
                "frame_%06d.png"
            )

            for i in range(frame_count):

                frame = self._create_frame(
                    scene,
                    i,
                    frame_count
                )

                frame.save(
                    os.path.join(
                        temp,
                        f"frame_{i:06d}.png"
                    )
                )

            command = [
                "ffmpeg",
                "-y",

                "-framerate",
                str(FPS),

                "-i",
                frame_pattern,

                "-c:v",
                "libx264",

                "-pix_fmt",
                "yuv420p",

                "-r",
                str(FPS),

                output_path
            ]

            subprocess.run(
                command,
                check=True
            )

    def generate(
        self,
        scenes,
        filename="benoit_video.mp4",
        audio_path=None
    ):

        output_path = os.path.join(
            self.output_dir,
            filename
        )

        with tempfile.TemporaryDirectory() as temp:

            scene_files = []

            # -----------------------------
            # Rendu des scènes
            # -----------------------------

            for i, scene in enumerate(scenes):

                scene_path = os.path.join(
                    temp,
                    f"scene_{i}.mp4"
                )

                print(
                    f"[VIDEO] Rendu scène "
                    f"{i + 1}/{len(scenes)}..."
                )

                self._render_scene(
                    scene,
                    scene_path
                )

                scene_files.append(
                    scene_path
                )

            # -----------------------------
            # Fichier concat
            # -----------------------------

            concat_file = os.path.join(
                temp,
                "concat.txt"
            )

            with open(
                concat_file,
                "w",
                encoding="utf-8"
            ) as f:

                for scene_file in scene_files:

                    safe_path = (
                        scene_file
                        .replace("\\", "/")
                    )

                    f.write(
                        f"file '{safe_path}'\n"
                    )

            # -----------------------------
            # Assemblage vidéo
            # -----------------------------

            silent_video = os.path.join(
                temp,
                "silent.mp4"
            )

            print(
                "[VIDEO] Assemblage des scènes..."
            )

            command = [
                "ffmpeg",
                "-y",

                "-f",
                "concat",

                "-safe",
                "0",

                "-i",
                concat_file,

                "-c",
                "copy",

                silent_video
            ]

            subprocess.run(
                command,
                check=True
            )

            # -----------------------------
            # Ajout audio
            # -----------------------------

            if audio_path:

                print(
                    "[VIDEO] Ajout de la voix..."
                )

                command = [
                    "ffmpeg",
                    "-y",

                    "-i",
                    silent_video,

                    "-i",
                    audio_path,

                    "-c:v",
                    "copy",

                    "-c:a",
                    "aac",

                    "-shortest",

                    output_path
                ]

                subprocess.run(
                    command,
                    check=True
                )

            else:

                os.replace(
                    silent_video,
                    output_path
                )

        print(
            f"[VIDEO] Vidéo créée : "
            f"{output_path}"
        )

        return output_path