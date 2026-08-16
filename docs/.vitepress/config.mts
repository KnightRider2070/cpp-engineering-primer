import { defineConfig } from 'vitepress'

const stages = [
  { id: 0, slug: 'environment-setup',          title: 'Environment Setup' },
  { id: 1, slug: 'print-an-empty-board',       title: 'Print an Empty Board' },
  { id: 2, slug: 'play-moves',                 title: 'Play Moves' },
  { id: 3, slug: 'create-gamestate',           title: 'Create GameState' },
  { id: 4, slug: 'validate-moves-and-errors',  title: 'Validate Moves + Errors' },
  { id: 5, slug: 'winner-detection',           title: 'Winner Detection' },
  { id: 6, slug: 'pointers-and-references',    title: 'Pointers & References' },
  { id: 7, slug: 'player-strategies',          title: 'Player Strategies' },
  { id: 8, slug: 'containerize-it',            title: 'Containerize It' },
]

export default defineConfig({
  title: 'C++ Engineering Primer',
  description: 'Build a Tic-Tac-Toe game. Learn the C++, Linux and Docker that interviews ask about.',
  base: '/cpp-engineering-primer/',
  lang: 'en-GB',
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,

  head: [
    ['meta', { name: 'theme-color', content: '#f2b705' }],
    ['link', {
      rel: 'icon',
      href: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='26' font-size='26'>%23%EF%B8%8F</text></svg>",
    }],
  ],

  themeConfig: {
    nav: [
      { text: 'Start', link: '/start/windows-wsl2' },
      { text: 'Stages', link: '/stages/' },
      { text: 'Reference', link: '/reference/contract' },
      { text: 'AI prompts', link: '/ai/prompts' },
      { text: 'Help', link: '/help/' },
    ],

    sidebar: [
      {
        text: 'Start here',
        items: [
          { text: 'How this course works', link: '/start/how-this-works' },
          { text: 'Windows + WSL2 setup', link: '/start/windows-wsl2' },
          { text: 'Your first run', link: '/start/first-run' },
        ],
      },
      {
        text: 'Stages',
        collapsed: false,
        items: [
          { text: 'The whole line', link: '/stages/' },
          ...stages.map((s) => ({
            text: `${s.id} — ${s.title}`,
            link: `/stages/${s.id}-${s.slug}`,
          })),
        ],
      },
      {
        text: 'Reference',
        collapsed: false,
        items: [
          { text: 'The contract', link: '/reference/contract' },
          { text: 'The build contract', link: '/reference/build-contract' },
          { text: 'Board output contract', link: '/reference/board-output-contract' },
          { text: 'HTTP API', link: '/reference/http-api' },
          { text: 'C++ notes', link: '/reference/cpp' },
          { text: 'Linux notes', link: '/reference/linux' },
          { text: 'Git notes', link: '/reference/git' },
          { text: 'CMake notes', link: '/reference/cmake' },
          { text: 'gdb notes', link: '/reference/gdb' },
          { text: 'Docker notes', link: '/reference/docker' },
        ],
      },
      {
        text: 'Working with AI',
        collapsed: false,
        items: [
          { text: 'The tutor contract', link: '/ai/tutor-contract' },
          { text: 'Prompt library', link: '/ai/prompts' },
        ],
      },
      {
        text: 'When something breaks',
        collapsed: false,
        items: [
          { text: 'All symptoms', link: '/help/' },
          { text: 'undefined reference to ...', link: '/help/undefined-reference' },
          { text: 'g++: command not found', link: '/help/gpp-command-not-found' },
          { text: 'localhost:8080 refused (from Windows)', link: '/help/localhost-refused-from-windows' },
          { text: 'Container runs, connection refused', link: '/help/container-connection-refused' },
          { text: 'I am stuck in a merge conflict', link: '/help/merge-conflict-recovery' },
          { text: 'My program hangs forever', link: '/help/program-hangs' },
        ],
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/KnightRider2070/cpp-engineering-primer' },
    ],

    search: { provider: 'local' },

    footer: {
      message: 'Your logic. Course transport.',
      copyright: 'cpp-engineering-primer',
    },

    outline: { level: [2, 3] },
  },
})
