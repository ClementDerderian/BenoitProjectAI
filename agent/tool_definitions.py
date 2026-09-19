TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Recherche des informations récentes ou spécifiques "
                "sur Internet. Utilise cet outil lorsque tu as besoin "
                "d'informations que tu ne connais pas."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "La recherche à effectuer."
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Nombre maximum de résultats.",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": (
                "Sauvegarde une information importante dans la mémoire "
                "persistante de Benoît."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Catégorie de la mémoire."
                    },
                    "content": {
                        "type": "string",
                        "description": "Information à mémoriser."
                    }
                },
                "required": ["category", "content"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_memory",
            "description": (
                "Recherche des informations précédemment mémorisées "
                "par Benoît."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Information recherchée."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Nombre maximum de souvenirs.",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        }
    }, {
    "type": "function",
    "function": {
        "name": "create_video",
        "description": (
            "Crée une vidéo verticale 9:16 à partir d'une liste "
            "de scènes. Utilise cet outil lorsqu'une vidéo doit "
            "être produite."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Titre de la vidéo."
                },
                "scenes": {
                    "type": "array",
                    "description": "Liste des scènes.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "duration": {
                                "type": "number"
                            },
                            "text": {
                                "type": "string"
                            },
                            "background": {
                                "type": "array",
                                "items": {
                                    "type": "integer"
                                }
                            },
                            "font_size": {
                                "type": "integer"
                            }
                        },
                        "required": [
                            "duration",
                            "text"
                        ]
                    }
                },
                "filename": {
                    "type": "string"
                }
            },
            "required": [
                "title",
                "scenes"
            ]
        }
    }
}
]