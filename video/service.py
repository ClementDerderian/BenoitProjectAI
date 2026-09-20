import os

from video.voice import VoiceGenerator
from video.generator import VideoGenerator
from video.scenes import Scene


class VideoService:

    def __init__(
        self,
        voice_reference="data/voice_reference.wav"
    ):

        print("[VIDEO] Initialisation...")

        self.voice = VoiceGenerator(
            voice_reference=voice_reference
        )

        self.generator = VideoGenerator()

        print("[VIDEO] Service vidéo prêt.")

    def create_video(
        self,
        title,
        scenes,
        filename="benoit_video.mp4"
    ):

        print()
        print("==============================")
        print("[VIDEO] Création d'une vidéo")
        print("==============================")
        print()

        # -----------------------------
        # 1. Transformer les scènes
        # -----------------------------

        parsed_scenes = []

        for scene in scenes:

            parsed_scenes.append(
                Scene(
                    duration=float(
                        scene["duration"]
                    ),
                    text=str(
                        scene["text"]
                    ),
                    background=tuple(
                        scene.get(
                            "background",
                            [10, 10, 20]
                        )
                    ),
                    font_size=int(
                        scene.get(
                            "font_size",
                            80
                        )
                    )
                )
            )

        # -----------------------------
        # 2. Construire le script
        # -----------------------------

        script = "\n\n".join(
            scene.text
            for scene in parsed_scenes
        )

        print("[VIDEO] Script :")
        print(script)
        print()

        # -----------------------------
        # 3. Génération de la voix
        # -----------------------------

        audio_filename = (
            os.path.splitext(filename)[0]
            + ".wav"
        )

        audio_path = os.path.join(
            "data/videos",
            audio_filename
        )

        voice_result = self.voice.generate(
            text=script,
            output_path=audio_path
        )

        print(
            f"[VIDEO] Voix : "
            f"{voice_result['duration']:.2f}s"
        )

        # -----------------------------
        # 4. Ajuster la durée vidéo
        # -----------------------------

        voice_duration = (
            voice_result["duration"]
        )

        requested_duration = sum(
            scene.duration
            for scene in parsed_scenes
        )

        # Si la voix est plus longue que
        # les scènes, on prolonge la dernière.
        if voice_duration > requested_duration:

            difference = (
                voice_duration
                - requested_duration
            )

            parsed_scenes[-1].duration += (
                difference
            )

        # -----------------------------
        # 5. Générer la vidéo
        # -----------------------------

        video_path = self.generator.generate(
            scenes=parsed_scenes,
            filename=filename,
            audio_path=audio_path
        )

        print()
        print(
            f"[VIDEO] Vidéo terminée : "
            f"{video_path}"
        )

        return {
            "title": title,
            "video": video_path,
            "audio": audio_path,
            "duration": voice_duration,
            "scenes": len(parsed_scenes)
        }