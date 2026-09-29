"""
TrendPilot CLI demo.

Run:  python demo.py
"""

from app.agent import run_content_agent
from app.memory import get_last_settings
from app.prompts import OUTPUT_TYPES, PLATFORM_RULES, TONE_PRESETS
from app.tools import (
    OllamaError,
    normalize_platform,
    normalize_tone,
    normalize_output_type,
)


def choose(title, options, default, normalizer=None):
    """
    Show a numbered menu. The user can type a number, type their own value,
    or press Enter for the default. Re-asks until the value is valid.
    """
    print(f"\n{title}")
    for i, option in enumerate(options, 1):
        marker = "  (default)" if option == default else ""
        print(f"  {i}. {option}{marker}")

    while True:
        raw = input("> ").strip()

        if not raw:
            return default
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]

        try:
            return normalizer(raw) if normalizer else raw
        except ValueError as e:
            print(f"  {e}")


def ask_tone(default):
    options = TONE_PRESETS + ["Custom"]
    while True:
        choice = choose("Choose tone:", options, default if default in options else "Professional")
        if choice != "Custom":
            return choice
        raw = input("Type your tone: ").strip()
        try:
            return normalize_tone(raw)
        except ValueError as e:
            print(f"  {e}")


def main():
    print("\n==============================================")
    print("        TRENDPILOT - LOCAL AI AGENT")
    print("==============================================")
    print("Powered by Ollama (local LLM)")
    print("==============================================")

    last = get_last_settings()

    while True:
        topic = ""
        while not topic:
            topic = input("\nEnter your topic: ").strip()
            if not topic:
                print("  Topic cannot be empty.")

        print("\nOptional: add real details about it (tools, dataset, results).")
        print("The agent only states facts you give it. Press Enter to skip.")
        details = input("Details: ").strip()

        platform = choose(
            "Choose platform:",
            list(PLATFORM_RULES),
            last.get("platform") or "LinkedIn",
            normalize_platform,
        )
        tone = ask_tone(last.get("tone") or "Professional")
        output_type = choose(
            "Choose output type:",
            OUTPUT_TYPES,
            last.get("output_type") or "Post + Reel Script",
            normalize_output_type,
        )

        try:
            run_content_agent(topic, platform, tone, output_type, details)
        except OllamaError as e:
            print(f"\n[Agent] ERROR: {e}")
            print("[Agent] Nothing was saved because generation failed.")
        except ValueError as e:
            print(f"\n[Agent] Invalid input: {e}")

        last = {"platform": platform, "tone": tone, "output_type": output_type}

        again = input("\nCreate another? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
