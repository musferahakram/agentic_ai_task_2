# TrendPilot - Local Agentic AI Assistant Using Ollama

AIRI Team PITB - AI Internship Task 2.

TrendPilot is a local AI agent that takes a topic, platform, tone and output type and
produces a complete content plan: idea, hook, caption, hashtags, short-video script,
title and thumbnail text, review comments, and a saved Markdown file. It runs fully on
your machine using a small local model through Ollama (default: `gemma3:4b`).

## Why this is an agent, not a chatbot

The agent does not just reply. For every request it:

1. Understands the goal and validates the input.
2. Reads memory (previous runs) and avoids repeating old angles.
3. Creates a plan from the requested output type.
4. Chooses and calls tools, logging each one (`[Tool Called]: ...`).
5. Runs automatic checks and an LLM review of its own output.
6. Improves the main content using the review.
7. Saves the result to files and writes the run to memory.

## Workflow

```
User input (topic, platform, tone, output type)
        |
        v
Validate input -> Read memory -> Create plan
        |
        v
Trend Idea Generator -> Idea Selector -> Target Audience Generator
        |
        v
Caption Writer (if Post) -> Hashtag Generator -> Reel Script Generator (if script)
        |
        v
Title + Thumbnail Generator
        |
        v
Content Validator (rules) -> Content Reviewer (LLM) -> Improve main content
        |
        v
File Saver -> Memory -> Final output
```

## Tools

| Tool | What it does |
|------|--------------|
| Trend Idea Generator | Creates 3 content ideas for the topic, avoiding recent topics from memory |
| Idea Selector | Picks the best idea and its hook |
| Target Audience Generator | Describes who the content is for |
| Caption Writer | Writes the post caption using platform rules |
| Hashtag Generator | Returns relevant hashtags, limited per platform |
| Reel Script Generator | 30-45 second script: hook, explanation, visual, closing line |
| Title + Thumbnail Generator | Suggests a title and short thumbnail text |
| Content Validator | Rule-based checks: length, invented percentages, placeholders, hashtag count |
| Content Reviewer | LLM review: hook, clarity, length, tone, hashtags, platform-readiness |
| File Saver | Saves results to `outputs/` (mandatory tool) |
| Memory | Reads and writes previous runs in `memory/history.json` |

## Supported platforms

LinkedIn, Instagram, X (Twitter), YouTube Shorts, TikTok, Facebook. Each has its own
caption length, hashtag count and writing style in `app/prompts.py`.

## Project structure

```
agentic_ai_task_2/
├── app/
│   ├── main.py        # entry point (re-exports the agent)
│   ├── agent.py       # agent workflow: plan, tool calls, review, improve, save
│   ├── tools.py       # all tools + Ollama connection + input validation
│   ├── memory.py      # read / write run history
│   └── prompts.py     # system prompt, platform rules, humor guide
├── outputs/
│   ├── generated_posts/     # caption + hashtags
│   ├── generated_scripts/   # short-video scripts
│   └── saved_results/       # full result of every run
├── memory/history.json
├── tests/
│   ├── test_cases.md        # test plan, results, error analysis
│   ├── run_tests.py         # runs the 10 test cases automatically
│   └── test_results.md      # created by run_tests.py
├── screenshots/
├── report/
├── demo.py            # CLI demo
├── requirements.txt
└── README.md
```

## Setup

1. Install Ollama from https://ollama.com and check it:

   ```
   ollama --version
   ```

2. Pull the model and test it:

   ```
   ollama pull gemma3:4b
   ollama run gemma3:4b
   ```

   If your machine cannot run it, use a smaller model (`llama3.2:3b`, `phi3:mini`,
   `qwen2.5:3b`) and set it before running:

   ```
   # Windows (PowerShell)
   $env:TRENDPILOT_MODEL = "llama3.2:3b"
   # Linux / macOS
   export TRENDPILOT_MODEL=llama3.2:3b
   ```

3. Install Python packages:

   ```
   pip install -r requirements.txt
   ```

## Run the demo

```
python demo.py
```

You will be asked for a topic, then platform, tone and output type (numbered menus;
press Enter to reuse your last choice). The agent prints every tool it calls, shows the
final result, and saves it under `outputs/`.

Example input:

```
Topic: YOLOv8 helmet detection project
Platform: LinkedIn
Tone: Professional
Output type: Post + Reel Script
```

Saved files:

```
outputs/saved_results/<topic>_<timestamp>.md
outputs/generated_posts/<topic>_<timestamp>.md
outputs/generated_scripts/<topic>_<timestamp>.md
```

## Run the tests

```
python tests/run_tests.py
```

This runs the 10 required test cases, saves 10 outputs, and writes
`tests/test_results.md`. Use `--only 3` to run a single test. See
`tests/test_cases.md` for the test plan, first-round results and error analysis.

## Memory

Each run adds one entry (topic, platform, tone, output type, idea, saved file) to
`memory/history.json`. At the start of every run the agent reads the last three runs,
uses their topics to avoid repeating angles, and the CLI uses your last platform, tone
and output type as defaults.

## Screenshots

- `screenshots/ollama_running.png` - model running in Ollama
- `screenshots/demo_output.png` - agent output in the terminal
- `screenshots/saved_file_output.png` - a saved result file

## Known limitations

- Small local models can still write generic hooks or weak jokes; the reviewer and
  validator reduce this but do not remove it.
- The validator catches invented percentages, not every unsupported claim.
- Generation of one full plan takes several model calls, so it can take a few minutes
  on a CPU-only laptop.

## Future improvements

User feedback loop, web search for trending topics, SQLite memory, Streamlit UI,
multi-agent workflow, PDF export, larger local models.
