<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <h1>Potter Plus</h1>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">HOME</RouterLink>
        <RouterLink to="/quiz">QUIZ</RouterLink>
        <RouterLink to="/about">ABOUT US</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style>
  @import '@/assets/base.css';
</style>
