from video.generator import VideoGenerator
from video.scenes import Scene


generator = VideoGenerator()


scenes = [

    Scene(
        duration=3,
        text="BENOÎT",
        background=(20, 30, 100),
        font_size=140
    ),

    Scene(
        duration=4,
        text="Voici notre moteur vidéo",
        background=(100, 20, 30),
        font_size=90
    ),

    Scene(
        duration=3,
        text="La prochaine étape : créer de vraies vidéos TikTok",
        background=(20, 100, 50),
        font_size=75
    ),

]


video = generator.generate(
    scenes,
    "test_video.mp4"
)

print()
print("VIDEO :", video)