<script setup lang="ts">
import { computed } from 'vue'
import { data as stages } from '../stages.data.mts'

const props = defineProps<{ stage: number }>()
const s = computed(() => stages.find((x) => x.id === props.stage)!)
</script>

<template>
  <div class="stage-header" v-if="s">
    <div class="meta">
      <span class="chip chip-stage">STAGE {{ s.id }}</span>
      <span class="chip">{{ s.tagline }}</span>
      <span class="chip">~{{ s.estimate }}</span>
    </div>
    <div class="unlocks">
      <strong>Unlocks:</strong> {{ s.unlocks }}
    </div>
  </div>
  <div class="hazard-rule" />
</template>
