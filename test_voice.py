from video.voice import VoiceGenerator


voice = VoiceGenerator()


result = voice.generate(
    text="""
    Bonjour, je suis Benoît.

    Aujourd'hui, je vais te montrer
    une idée de business numérique
    que tu peux lancer avec très peu d'argent.
    """,

    output_path="data/benoit.mp3"
)


print()
print("RESULTAT :")
print(result)