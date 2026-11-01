# Install sfx-generator (instructions for an AI coding agent)

You are reading this because someone pasted this repository's URL into Claude Code, Codex or a similar agent and
asked for it to be installed. Follow these steps in order. Everything here runs on the user's machine; nothing is
sent anywhere. The repository is `thisisvela/sfx-generator-skill` on GitHub (Apache 2.0).

What you are installing:

- the `sfx` command (a Python package: deterministic sound-effect recipes, a renderer, an inspector, a tuning page);
- two skills, `make-sound-effect` and `create-sound-recipe`, so the agent can turn a sentence into a finished sound.

## 1. Ask one question

Ask the user:

> Install the sound effects skills **for this project** (added to the repository, so collaborators get them) or
> **for you** (available in every project on this machine)?

Remember the answer as `SCOPE = project` or `SCOPE = user`. Do not ask anything else; take the defaults below.

## 2. Install the `sfx` command (isolated, once per machine)

Python 3.10 or newer is required. Check with `python --version` (or `python3`). If it is missing, stop and tell the
user to install Python 3.10 or newer, then continue.

Install the package as an isolated tool so it never touches the project's own dependencies. Try these in order and
stop at the first that works:

```bash
uv tool install "sfx-generator[ffmpeg] @ git+https://github.com/thisisvela/sfx-generator-skill"
```

```bash
pipx install "sfx-generator[ffmpeg] @ git+https://github.com/thisisvela/sfx-generator-skill"
```

If neither `uv` nor `pipx` is on PATH, make a private virtual environment and install there:

```bash
python -m venv ~/.sfx-generator/venv
~/.sfx-generator/venv/bin/pip install "sfx-generator[ffmpeg] @ git+https://github.com/thisisvela/sfx-generator-skill"
```

(On Windows the paths are `%USERPROFILE%\.sfx-generator\venv\Scripts\pip.exe` and `...\Scripts\sfx.exe`.) In that case
`sfx` is `~/.sfx-generator/venv/bin/sfx`; tell the user, and use that full path wherever these instructions say `sfx`.

The `[ffmpeg]` extra installs a static ffmpeg so OGG and MP3 export work without a system ffmpeg.

Verify:

```bash
sfx --version
sfx list
```

`sfx list` must end with `99 sounds`. If `sfx` is not found after a `uv tool` or `pipx` install, the tool's bin
directory is not on PATH: run `uv tool update-shell` or `pipx ensurepath`, then open a new shell.

## 3. Install the skills

### Claude Code

Run from the shell (Claude Code v2.1.292 or later):

```bash
claude plugin install sfx-generator --marketplace thisisvela/sfx-generator-skill --scope project
```

Use `--scope user` when `SCOPE = user`. On an older Claude Code, run the two steps instead:

```bash
claude plugin marketplace add thisisvela/sfx-generator-skill
claude plugin install sfx-generator@sfx-generator --scope project
```

If the `claude` command is not on PATH (for example inside the desktop app), tell the user to run this in their
Claude Code session and pick the scope in the dialog:

```text
/plugin install sfx-generator --marketplace thisisvela/sfx-generator-skill
```

The skills then appear as `/sfx-generator:make-sound-effect` and `/sfx-generator:create-sound-recipe`, and Claude
picks them up on its own when a request matches. A new session, or `/reload-plugins`, activates them.

### Codex (CLI, IDE extension or app)

Codex discovers skills in `.agents/skills` of a repository and in `~/.agents/skills` for the user.

For `SCOPE = project`, copy the skills into the project so they travel with it:

```bash
git clone --depth 1 https://github.com/thisisvela/sfx-generator-skill /tmp/sfx-generator-skill
mkdir -p .agents/skills
cp -r /tmp/sfx-generator-skill/skills/make-sound-effect .agents/skills/
cp -r /tmp/sfx-generator-skill/skills/create-sound-recipe .agents/skills/
rm -rf /tmp/sfx-generator-skill
```

For `SCOPE = user`, keep a clone and link it, so `git pull` updates the skills:

```bash
git clone https://github.com/thisisvela/sfx-generator-skill ~/.sfx-generator/repo
mkdir -p ~/.agents/skills
ln -s ~/.sfx-generator/repo/skills ~/.agents/skills/sfx-generator
```

Windows (PowerShell), a junction instead of a symlink:

```powershell
git clone https://github.com/thisisvela/sfx-generator-skill "$env:USERPROFILE\.sfx-generator\repo"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills" | Out-Null
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\sfx-generator" "$env:USERPROFILE\.sfx-generator\repo\skills"
```

Codex detects new skills on its own; if they do not appear, restart it. They are invoked as `$make-sound-effect`
and `$create-sound-recipe`, or implicitly when a request matches.

### Any other agent

Copy `skills/make-sound-effect` and `skills/create-sound-recipe` from the repository to wherever the agent reads
`SKILL.md` folders from. The skills are plain Markdown and assume only that `sfx` runs from a shell.

## 4. Smoke test

```bash
sfx make "a soft click" -o out/sfx-install-test -n 3 --formats wav
```

It must print three variants with their numbers and the path of an audition page. Delete `out/sfx-install-test`
afterwards unless the user wants to keep it.

## 5. Tell the user how to use it

Report, in a few lines:

- `sfx` is installed (say where, if it is the venv fallback) and the skills are installed at the chosen scope.
- They can now ask, in their own words: "make a quick whoosh for a slide transition", "a soft two-note success
  chime, about half a second", "a notification a fifth up, bright and dry", "open the tuning page for the ping".
- Generated sounds land in `assets/sfx/<name>/` inside their project unless they say otherwise, as WAV, OGG and
  MP3 with a preset JSON that recreates them.
- The tuning page is `sfx tune <preset or id>`: a local page at http://127.0.0.1:8765 with sliders for every
  parameter. The skill starts it when they ask to adjust a sound by hand.
- The library of 99 ready sounds and the docs are at https://thisisvela.github.io/sfx-generator-skill/.

## Updating

- `uv tool upgrade sfx-generator` or `pipx upgrade sfx-generator` (or re-run the pip line in the venv fallback).
- Claude Code: `claude plugin update sfx-generator@sfx-generator`.
- Codex, user scope: `git -C ~/.sfx-generator/repo pull`. Project scope: repeat the copy in step 3.

## Uninstalling

- `uv tool uninstall sfx-generator` or `pipx uninstall sfx-generator`, or delete `~/.sfx-generator`.
- Claude Code: `claude plugin uninstall sfx-generator@sfx-generator` (add `--scope project` if installed there).
- Codex: delete `.agents/skills/make-sound-effect` and `.agents/skills/create-sound-recipe` from the project, or
  remove the `~/.agents/skills/sfx-generator` link.
