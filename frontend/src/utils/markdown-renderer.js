import MarkdownIt from 'markdown-it'
import MarkdownItContainer from 'markdown-it-container'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'

const md = new MarkdownIt({
  html: true,          // 允许 HTML（用于 <details> <summary>）
  linkify: true,
  typographer: true,
  highlight: (str, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return ''
  }
})

// 解析 ::: tabs 容器
let tabIndex = 0;
md.use(MarkdownItContainer, 'tabs', {
  validate: function(params) {
    return params.trim().match(/^tabs\s*(.*)$/);
  },
  render: function (tokens, idx) {
    if (tokens[idx].nesting === 1) {
      tabIndex++;
      return `<div class="tabs-container" data-tab-group="${tabIndex}">\n<div class="tabs-nav-placeholder"></div>\n<div class="tabs-content">\n`;
    } else {
      return '</div>\n</div>\n';
    }
  }
});

// 解析 ::: tabpane 容器
md.use(MarkdownItContainer, 'tabpane', {
  validate: function(params) {
    return params.trim().match(/^tabpane\s+(.*)$/);
  },
  render: function (tokens, idx) {
    var m = tokens[idx].info.trim().match(/^tabpane\s+(.*)$/);
    if (tokens[idx].nesting === 1) {
      return '<div class="tab-pane" data-title="' + md.utils.escapeHtml(m[1]) + '">\n';
    } else {
      return '</div>\n';
    }
  }
});

export function renderMarkdown(text) {
  // 确保 <summary> 和 ::: tabs 之间有空行，否则 markdown-it 不会解析内容
  let processedText = text.replace(/<\/summary>\s*:::/g, '</summary>\n\n:::');
  
  // 处理 <summary> 内部的简易 Markdown (因为 HTML 块内的内容默认不解析)
  processedText = processedText.replace(/<summary>(.*?)<\/summary>/g, (match, p1) => {
    let inner = p1.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    inner = inner.replace(/\*(.*?)\*/g, '<em>$1</em>');
    inner = inner.replace(/_(.*?)_/g, '<em>$1</em>');
    inner = inner.replace(/`(.*?)`/g, '<code>$1</code>');
    // 使用 <span> 包裹，防止 Flex 的 space-between 布局导致元素被异常分离
    return `<summary><span>${inner}</span></summary>`;
  });

  // 处理雷达提取的句子块，变成可点击的联动按钮
  processedText = processedText.replace(/>\s*【雷达提取】(.*?)(?=\n|$)/g, (match, sentence) => {
    const cleanSentence = sentence.trim();
    const escapedSentence = cleanSentence.replace(/"/g, '&quot;');
    return `> <div class="radar-box"><span class="radar-text">${cleanSentence}</span><button class="radar-btn" data-sentence="${escapedSentence}">一键精读 🎯</button></div>`;
  });

  // 处理大模型可能将 `==` 错误放在 `::: tabs` 同一行的问题
  processedText = processedText.replace(/:::\s*tabs\s*==/g, '::: tabs\n==');
  let lines = processedText.split('\n');
  let resultLines = [];
  let currentTabOpen = false;
  let inTabs = false;

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    
    if (line.startsWith('::: tabs')) {
      inTabs = true;
      // 使用 4 个冒号作为外部容器，避免与内部的 3 个冒号冲突
      resultLines.push(':::: tabs');
      continue;
    }
    
    // 遇到结束标志，如果里面有未关闭的 tabpane，先关闭
    if (line.trim() === ':::' && inTabs) {
      if (currentTabOpen) {
        resultLines.push(':::'); // 关闭 tabpane
        currentTabOpen = false;
      }
      inTabs = false;
      resultLines.push('::::'); // 关闭 tabs
      continue;
    }
    
    if (inTabs && line.startsWith('== ')) {
      let title = line.substring(3).trim();
      if (currentTabOpen) {
        resultLines.push(':::'); // 关闭上一个 tabpane
      }
      resultLines.push(`::: tabpane ${title}`);
      currentTabOpen = true;
      continue;
    }
    
    resultLines.push(line);
  }
  
  if (currentTabOpen) {
    resultLines.push(':::');
  }
  if (inTabs) {
    resultLines.push('::::');
  }

  return md.render(resultLines.join('\n'));
}
