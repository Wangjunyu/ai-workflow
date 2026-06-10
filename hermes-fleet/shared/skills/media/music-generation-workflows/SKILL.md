---
name: music-generation-workflows
description: "Use when writing songs, crafting AI music prompts, or generating music with hosted or local text-to-music systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [music, songwriting, lyrics, ai-music, suno, local-generation]
    related_skills: [audiocraft-audio-generation]
---

# Music Generation Workflows

## Overview

This umbrella skill covers the class of music-generation tasks that move between songwriting craft, prompt design, lyric structure, and concrete generation backends. The broad class is more discoverable than splitting "write better lyrics" and "use a specific generator" into separate micro-skills.

Use this skill for both:
- front-end creative work: hooks, lyrics, structure, parody/adaptation, vocal direction
- back-end generation work: selecting and operating a model or service such as Suno-like tools or local open-source stacks

## When to Use

- Writing or revising song lyrics
- Designing prompts/tags for AI music generation
- Adapting an existing song structure or parody
- Choosing between hosted and local generation workflows
- Running an open-source song generator from lyrics + tags

## Lane A — Songwriting and prompt craft

Core topics:
- song structure
- rhyme, meter, stress, and singability
- emotional arc and dynamics
- hook design
- parody/adaptation constraints
- phonetic spelling for AI vocalists

Guiding rule: describe the performance journey, not just the genre label.

Useful prompt ingredients:
- genre
- mood
- era
- instrumentation
- vocal persona
- production texture
- dynamic arc

## Lane B — Generator/backend selection

Choose backend based on constraints:
- hosted tool when speed and convenience matter
- local open-source backend when the user wants controllability, offline use, or reproducibility

For local systems, verify:
- hardware/VRAM fit
- Python/runtime compatibility
- model checkpoints
- dependency compatibility
- generation command and output path

## Subsection absorbed from narrower songwriting skill

For lyric and prompt work:
- map structure before rewriting an existing song
- match stressed syllables more carefully than raw syllable counts
- use structural tags and dynamic guidance in generated-song lyrics
- build a clear vocal persona
- test unusual proper nouns and pronunciations early

## Subsection absorbed from narrower local generator skill

For local song generation backends such as HeartMuLa-style systems:
- treat install/patch/checkpoint steps as backend-specific support detail, not as a standalone class of skill
- verify Python version and VRAM budget before installation
- validate imports and run a smallest-possible generation first
- keep backend quirks in support files rather than spawning one skill per model family

## Common Pitfalls

1. Treating lyric craft and generator usage as unrelated; in practice they are one workflow.
2. Giving only a genre label instead of a dynamic arc and vocal persona.
3. Ignoring pronunciation constraints for AI singers.
4. Choosing a local backend without checking hardware and dependency fit.
5. Creating a separate skill for each model/backend when the maintainer really wants one music-generation umbrella plus backend notes.

## Verification Checklist

- [ ] Task classified correctly as songwriting, generation, or both
- [ ] Lyrics/prompt describe structure and dynamics, not only genre
- [ ] Backend choice matches user constraints
- [ ] Local backend prerequisites verified before install/run
- [ ] Output path or generated artifact verified when generation is executed
