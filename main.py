import json
from pathlib import Path

from agent.brain import BenoitBrain
from agent.memory import BenoitMemory
from agent.tools import BenoitTools
from agent.tool_definitions import TOOLS


def load_system_prompt():
    return Path(
        "prompts/system.txt"
    ).read_text(encoding="utf-8")


def execute_tool(tool_name, arguments, tools):
    if tool_name == "web_search":
        return tools.web_search(
            arguments["query"],
            arguments.get("max_results", 5)
        )

    if tool_name == "save_memory":
        return tools.save_memory(
            arguments["category"],
            arguments["content"]
        )

    if tool_name == "search_memory":
        return tools.search_memory(
            arguments["query"],
            arguments.get("limit", 10)
        )
    
    if tool_name == "create_video":

        return tools.create_video(
        arguments["title"],
        arguments["scenes"],
        arguments.get(
            "filename",
            "benoit_video.mp4"
        )
    )

    return f"Outil inconnu : {tool_name}"


def run_agent(brain, tools, messages):

    max_iterations = 10

    for _ in range(max_iterations):

        message = brain.ask(
            messages,
            tools=TOOLS
        )

        tool_calls = message.get("tool_calls")

        if not tool_calls:

            answer = message.get("content", "")

            messages.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        messages.append(message)

        for tool_call in tool_calls:

            function = tool_call["function"]

            tool_name = function["name"]

            arguments = function.get("arguments", {})

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            print(
                f"\n[Benoît utilise : {tool_name}]"
            )

            print(
                f"[Arguments : {arguments}]"
            )

            result = execute_tool(
                tool_name,
                arguments,
                tools
            )

            messages.append({
                "role": "tool",
                "content": str(result)
            })

    return "J'ai atteint la limite d'actions pour cette tâche."


def main():

    print()
    print("======================================")
    print("          BENOÎT AI - V0.2")
    print("======================================")
    print("Cerveau : Qwen3")
    print("Mémoire : SQLite")
    print("Outils : Recherche Web + Mémoire")
    print("Mode : local")
    print()
    print("Benoît est prêt.")
    print("Tape 'quit' pour quitter.")
    print()

    brain = BenoitBrain()

    memory = BenoitMemory()

    tools = BenoitTools(memory)

    system_prompt = load_system_prompt()

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    while True:

        user_input = input("Toi > ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("Benoît > À bientôt.")
            break

        if not user_input:
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        try:

            answer = run_agent(
                brain,
                tools,
                messages
            )

            print()
            print("Benoît >")
            print(answer)
            print()

            memory.save(
                "conversation",
                f"Utilisateur : {user_input}\n"
                f"Benoît : {answer}"
            )

        except Exception as error:

            print()
            print("ERREUR :", error)
            print()


if __name__ == "__main__":
    main()