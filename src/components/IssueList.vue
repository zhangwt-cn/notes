<template>
    <div class="issues-list">
        <div class="search-box">
            <input type="text" v-model="searchTerm" placeholder="Search issues...">
        </div>
        <ul class="list-style-none">
            <li v-for="(issue, index) in filteredIssues" :key="issue.id" class="Box">
                <IssueDetail :issue="issue"/>
            </li>
        </ul>
        <div class="pagination">
            <button :disabled="page === 1" @click="page--">Prev</button>
            <span>{{ page }}</span>
            <button :disabled="page === totalPages" @click="page++">Next</button>
        </div>
    </div>
</template>

<script>
import IssueDetail from './IssueDetail.vue';

export default {
    components: {
        IssueDetail,
    },

    data() {
        return {
            issues: [],
            searchTerm: '',
            page: 1,
            perPage: 10,
        };
    },
    created() {
        this.getGitHubIssues();
    },
    computed: {
        filteredIssues() {
            return this.issues.filter(issue => {
                return issue.title.toLowerCase().includes(this.searchTerm.toLowerCase());
            }).slice((this.page - 1) * this.perPage, this.page * this.perPage);
        },
        totalPages() {
            return Math.ceil(this.issues.length / this.perPage);
        },
    },
    methods: {
        async getGitHubIssues() {
            const response = await fetch('https://api.github.com/repos/zhangwt-cn/notes/issues');
            this.issues = await response.json();
        },

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
    },
};
</script>

<style>
/* Import Primer CSS styles */
@import '@primer/css/index.scss';

/* Apply styles to GitHub Issues list */
.issues-list {
    margin-top: 24px;
}

.search-box {
  display: flex;
  margin-bottom: 16px;
}

input[type="text"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px 0 0 5px;
  width: 200px;
}
</style>