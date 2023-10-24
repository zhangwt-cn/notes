<template>
    <div class="Box-header">
        <h3 class="Box-title">
            <a :href="issue.html_url" target="_blank">{{ issue.title }}</a>
        </h3>
    </div>
    <div class="Box-body markdown-body" v-html="renderMarkdown(issue.body)">
    </div>
    <div class="Box-footer">
        <a :href="issue.html_url" target="_blank">View on GitHub</a>
    </div>
</template>

<script>
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js/lib/core';

// 导入您需要使用的语言模块
import javascript from 'highlight.js/lib/languages/javascript';
import css from 'highlight.js/lib/languages/css';
import html from 'highlight.js/lib/languages/xml';

// 将语言模块注册到 highlight.js 中
hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('css', css);
hljs.registerLanguage('html', html);


export default {
    name: 'IssueDetail',
    props: {
    issue: {
      type: Object,
      required: true,
    }
  },


    methods: {
        renderMarkdown(markdown) {
            const renderer = new MarkdownIt({
                html: true,
                linkify: true,
                typographer: true,
                highlight: function (code, lang) {
                    if (lang && hljs.getLanguage(lang)) {
                        return hljs.highlight(lang, code).value;
                    } else {
                        return hljs.highlightAuto(code).value;
                    }
                }
            });
            return renderer.render(markdown);
        },
    }
}
</script>

<style>
@import '@primer/css/index.scss';

.Box {
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    margin-bottom: 16px;
}

.Box-header {
    background-color: #f6f8fa;
    border-bottom: 1px solid #e1e4e8;
    padding: 8px 16px;
}

.Box-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
}

.Box-body {
    padding: 16px;
}

.Box-footer {
    background-color: #f6f8fa;
    border-top: 1px solid #e1e4e8;
    padding: 8px 16px;
    text-align: right;
}

.Box-footer a {
    color: #0366d6;
    text-decoration: none;
}

.Box-footer a:hover {
    text-decoration: underline;
}

.pagination {
    margin-top: 16px;
    text-align: center;
}

.pagination button {
    background-color: #f6f8fa;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    color: #24292e;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    margin: 0 4px;
    padding: 8px 16px;
}

.pagination button:hover {
    background-color: #eaecef;
}

.pagination button:disabled {
    background-color: #f6f8fa;
    border-color: #e1e4e8;
    color: #6a737d;
    cursor: not-allowed;
}

.pagination span {
    font-size: 14px;
    font-weight: 600;
    margin: 0 8px;
}

/* Apply styles to GitHub-style Markdown */
.markdown-body {
    font-size: 16px;
    line-height: 1.5;
    color: #24292e;

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        font-weight: 600;
        margin-top: 24px;
        margin-bottom: 16px;
    }

    h1 {
        font-size: 32px;
    }

    h2 {
        font-size: 24px;
    }

    h3 {
        font-size: 20px;
    }

    h4 {
        font-size: 16px;
    }

    h5 {
        font-size: 14px;
    }

    h6 {
        font-size: 12px;
    }

    p {
        margin-top: 0;
        margin-bottom: 16px;
    }

    ul,
    ol {
        margin-top: 0;
        margin-bottom: 16px;
        padding-left: 24px;
    }

    li {
        margin-bottom: 8px;
    }

    a {
        color: #0366d6;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    pre {
        margin-top: 0;
        margin-bottom: 16px;
        padding: 16px;
        background-color: #f6f8fa;
        border-radius: 6px;
        overflow-x: auto;
    }

    code {
        font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
        font-size: 14px;
        background-color: #f6f8fa;
        padding: 3px 6px;
        border-radius: 3px;
    }

    blockquote {
        margin-top: 0;
        margin-bottom: 16px;
        padding: 0 16px;
        border-left: 4px solid #dfe2e5;
        color: #6a737d;
    }

    table {
        margin-top: 0;
        margin-bottom: 16px;
        border-collapse: collapse;
        width: 100%;
    }

    th,
    td {
        padding: 6px 13px;
        border: 1px solid #dfe2e5;
    }

    th {
        font-weight: 600;
    }

    img {
        max-width: 100%;
        height: auto;
    }
}
</style>