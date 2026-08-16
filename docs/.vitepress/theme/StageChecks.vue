<script setup lang="ts">
import { computed } from 'vue'
import { data as stages } from '../stages.data.mts'

const props = defineProps<{ stage: number }>()
const s = computed(() => stages.find((x) => x.id === props.stage)!)
</script>

<template>
  <ul class="checks" v-if="s">
    <li v-for="(c, i) in s.checks" :key="i">{{ c }}</li>
  </ul>
  <p>
    Verify with <code>./ttt check {{ stage }}</code>.
    Add <code>--explain</code> and it shows you exactly what it compiled, what
    it typed in, and what it saw.
  </p>
</template>
