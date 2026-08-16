---
title: Prompt library
---

<script setup>
import { data as stages } from '../.vitepress/stages.data.mts'
</script>

# Prompt library

Three prompts per stage. Each one is built from that stage's knowledge bounds,
so the assistant knows what you have learned and what it must not use.

From the terminal:

```bash
./ttt prompt 5           # list stage 5's prompts
./ttt prompt 5 2         # print one, ready to paste
./ttt prompt 5 2 | clip.exe   # on WSL2: straight to the Windows clipboard
```

All three shapes recur at every stage:

1. **Explain this error** — paste the compiler or sanitizer output and get it
   read back to you, rather than fixed for you.
2. **Review my approach, don't write it** — asks for questions back, not code.
3. **Quiz me** — Socratic, and the closest thing here to interview practice.

They all sit on top of [the tutor contract](/ai/tutor-contract).

<div v-for="s in stages" :key="s.id">
  <h2 :id="'stage-' + s.id">Stage {{ s.id }} — {{ s.title }}</h2>
  <p><em>Assumes you know:</em> {{ s.knows.join(', ') }}.<br>
     <em>Will avoid:</em> {{ s.notYet.join(', ') }}.</p>
  <ul>
    <li v-for="p in s.prompts" :key="p.id">
      <strong>{{ p.title }}</strong> — <code>./ttt prompt {{ s.id }} {{ p.id }}</code>
    </li>
  </ul>
</div>

## Using them well

**Paste the actual output.** Not "I got an error" — the whole message, including
the part you think is noise. The line numbers matter.

**Answer the question it asks back.** These prompts all end by asking what you
expected to happen. Skipping past that to demand the fix wastes the only part
that teaches you anything.

**Do not paste the answer into your editor.** If it gave you code, retype it.
You will notice the parts you do not understand, which is the point.
