<script setup lang="ts">
import { useData, withBase } from 'vitepress'
import { data as stages } from '../stages.data.mts'
</script>

<template>
  <ul class="line">
    <li class="line-station" v-for="s in stages" :key="s.id">
      <span class="line-num">{{ s.id }}</span>
      <a :href="withBase(`/stages/${s.id}-${s.slug}`)">{{ s.title }}</a>
      <span class="line-tag">{{ s.tagline }}</span>
    </li>
  </ul>
</template>
