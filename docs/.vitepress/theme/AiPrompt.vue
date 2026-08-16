<script setup lang="ts">
import { computed } from 'vue'
import { data as stages } from '../stages.data.mts'

const props = defineProps<{ stage: number; id: number }>()
const s = computed(() => stages.find((x) => x.id === props.stage)!)
const p = computed(() => s.value?.prompts?.find((x) => x.id === props.id))

// The same preamble ./ttt prompt builds, so the page and the CLI agree.
const composed = computed(() => {
  if (!s.value || !p.value) return ''
  const knows = s.value.knows.join(', ')
  const notYet = s.value.notYet.join(', ')
  return (
`You are my tutor. Follow the rules in docs/ai/tutor-contract.md -- especially:
do not give me a complete implementation unless I have used hint levels 1
through 4 and then explicitly say "give me the answer", and prefer syntax
examples that are NOT about tic-tac-toe so I still have to apply the idea
myself.

I am on Stage ${s.value.id} (${s.value.title}) of a C++ course.

At this point I know: ${knows}.
I have NOT learned yet: ${notYet}.
Do not use anything from that list in your answer.

Ask me what I expected to happen before you tell me anything.

---

` + p.value.body)
})
</script>

<template>
  <div class="prompt-box" v-if="p">
    <div class="prompt-head">
      <span>{{ p.title }}</span>
      <span class="cmd">./ttt prompt {{ stage }} {{ id }}</span>
    </div>
    <pre>{{ composed }}</pre>
  </div>
</template>
