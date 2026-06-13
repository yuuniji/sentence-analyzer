import { renderMarkdown } from './src/utils/markdown-renderer.js'

const text = `
<details>
<summary>Palmistry is probably...</summary>

::: tabs
== 完整翻译
意译：手相术

== 语义/意群拆分
Palmistry

:::
</details>
`

console.log(renderMarkdown(text))
