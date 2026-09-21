# IELTS Claude Skills — Project Instructions

## Project Overview

An IELTS prep AI coaching system (vPro) made up of 8 Claude Code Skills.

## Workflow

### Day-to-day development

- Working directory: `D:\Ielts\`

- No remote repository configured yet — this is a local-only working copy.

### When a usage issue comes up

When a user runs into a problem while using a skill (a bug, missing feature, or UX issue), handle it as follows:

1. Fix the issue in the working directory

2. Sync to `~/.claude/skills/`:

   ```bash
   cp -r ielts ielts-writing ielts-reading ielts-speaking ielts-listening ielts-vocab ielts-diagnosis ielts-dashboard shared dashboard ~/.claude/skills/
   ```

3. Commit locally (no remote to push to yet):

   ```bash
   git add -A && git commit -m "<description of the change>"
   ```

4. Tell the user what was fixed

### Data layer

- CLI script: `shared/ielts_cli.py` (Python stdlib-only)

- User data is stored in `~/.ielts/`, fully local, no cloud

- The CLI path is referenced within skills as: `python3 ~/.claude/skills/shared/ielts_cli.py`
