// Reads course/stages/*.json at build time.
//
// This is the same data `./ttt` reads. Neither the site nor the CLI owns the
// text -- if they ever disagree, one of them is reading a stale file.

import fs from 'node:fs'
import path from 'node:path'
import { defineLoader } from 'vitepress'

const STAGES_DIR = path.resolve(__dirname, '../../course/stages')

export interface Stage {
  id: number
  slug: string
  title: string
  tagline: string
  estimate: string
  unlocks: string
  objective: string
  creates: string[]
  concepts: { cpp: string[]; linux: string[]; git: string[] }
  knows: string[]
  notYet: string[]
  checks: string[]
  hints: string[]
  prompts: { id: number; title: string; body: string }[]
}

declare const data: Stage[]
export { data }

export default defineLoader({
  watch: ['../../course/stages/*.json'],
  load(): Stage[] {
    return fs
      .readdirSync(STAGES_DIR)
      .filter((f) => f.endsWith('.json'))
      .sort()
      .map((f) => JSON.parse(fs.readFileSync(path.join(STAGES_DIR, f), 'utf-8')))
  },
})
