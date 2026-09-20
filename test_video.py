from video.service import VideoService


service = VideoService()


result = service.create_video(
    title="3 idées de business avec l'IA",
    
    script="""
    Voici trois idées de business que tu peux lancer
    avec l'intelligence artificielle.

    Première idée : créer des vidéos automatiquement
    pour les réseaux sociaux.

    Deuxième idée : créer des outils spécialisés
    pour les créateurs de contenu.

    Troisième idée : automatiser des tâches répétitives
    pour les petites entreprises.

    Le plus intéressant est de commencer petit,
    tester rapidement,
    puis automatiser ce qui fonctionne.
    """,

    filename="premiere_video_benoit.mp4"
)


print()
print("========== RESULTAT ==========")
print(result)