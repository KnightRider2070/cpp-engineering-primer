<script setup lang="ts">
// Hint level 1 renders inline. Levels 2-4 render as a stub that points at the
// terminal.
//
// This is deliberate. A <details> block is not a gate -- one click opens all
// four, and the CLI's record of what you opened becomes fiction. Keeping the
// later hints behind `./ttt hint` means the progression is real, and it keeps
// pulling you back to the terminal, which is where the course happens.
import { computed } from 'vue'
import { data as stages } from '../stages.data.mts'

const props = defineProps<{ stage: number; level: number }>()
const s = computed(() => stages.find((x) => x.id === props.stage)!)
const text = computed(() => s.value?.hints?.[props.level - 1] ?? '')

const LABELS = ['Direction', 'Decomposition', 'Pseudocode', 'C++ specifics']
const label = computed(() => LABELS[props.level - 1] ?? '')
</script>

<template>
  <div v-if="level === 1" class="hint">
    <div class="hint-label">Hint 1 — {{ label }}</div>
    <div class="hint-body">{{ text }}</div>
  </div>

  <div v-else class="hint hint-locked">
    <div class="hint-label">Hint {{ level }} — {{ label }}</div>
    <div>
      In your terminal: <code>./ttt hint {{ stage }} {{ level }}</code>
    </div>
  </div>
</template>
