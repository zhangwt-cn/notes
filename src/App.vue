<script setup>
import IssueList from './components/IssueList.vue';
</script>

<template>
  <header>
    <h1>GitHub Issue Browser</h1>
  </header>

  <main>
    <IssueList />
  </main>
</template>

<style>
/* Import Primer CSS styles */
@import '@primer/css/index.scss';


main, header {
  max-width: 980px;
  margin: 0 auto;
  padding: 24px;
}
</style>
