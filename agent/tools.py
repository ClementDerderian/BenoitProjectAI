from ddgs import DDGS
from video.service import VideoService

class BenoitTools:

    def __init__(self, memory):
        self.memory = memory
        self.video = VideoService()
    def web_search(self, query, max_results=5):
        """
        Recherche des informations sur Internet.
        """

        try:
            results = DDGS().text(
                query,
                max_results=max_results
            )

            if not results:
                return "Aucun résultat trouvé."

            output = []

            for result in results:
                title = result.get("title", "")
                url = result.get("href", "")
                body = result.get("body", "")

                output.append(
                    f"TITRE: {title}\n"
                    f"URL: {url}\n"
                    f"DESCRIPTION: {body}"
                )

            return "\n\n".join(output)

        except Exception as error:
            return f"Erreur de recherche : {error}"

    def save_memory(self, category, content):
        return self.memory.save(category, content)

    def search_memory(self, query, limit=10):
        return self.memory.search(query, limit)
    def create_video(
    self,
    title,
    scenes,
    filename="benoit_video.mp4"
    ):

        return self.video.create_video(
        title,
        scenes,
        filename
    )