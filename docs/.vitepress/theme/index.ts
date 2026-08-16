import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'

import StageHeader from './StageHeader.vue'
import StageChecks from './StageChecks.vue'
import Hint from './Hint.vue'
import AiPrompt from './AiPrompt.vue'
import StageLine from './StageLine.vue'

import './factory.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('StageHeader', StageHeader)
    app.component('StageChecks', StageChecks)
    app.component('Hint', Hint)
    app.component('AiPrompt', AiPrompt)
    app.component('StageLine', StageLine)
  },
} satisfies Theme
