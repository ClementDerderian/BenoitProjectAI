from video.generator import VideoGenerator
from video.scenes import Scene


class VideoService:

    def __init__(self):
        self.generator = VideoGenerator()

    def create_video(
        self,
        title,
        scenes,
        filename="benoit_video.mp4"
    ):

        parsed_scenes = []

        for scene in scenes:

            parsed_scenes.append(
                Scene(
                    duration=scene["duration"],
                    text=scene["text"],
                    background=tuple(
                        scene.get(
                            "background",
                            [10, 10, 20]
                        )
                    ),
                    font_size=scene.get(
                        "font_size",
                        80
                    )
                )
            )

        path = self.generator.generate(
            parsed_scenes,
            filename
        )

        return {
            "title": title,
            "path": path,
            "duration": sum(
                scene.duration
                for scene in parsed_scenes
            ),
            "scenes": len(parsed_scenes)
        }