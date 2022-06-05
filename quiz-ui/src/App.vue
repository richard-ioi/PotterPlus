<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <h1>Potter Plus</h1>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">HOME</RouterLink>
        <div class="dropdown">
          <a class="dropbtn">QUIZ</a>
          <div class="dropdown-content">
            <RouterLink to="questions">House</RouterLink>
            <RouterLink to="questions" class = "disabledlink" >Patronus</RouterLink>
          </div>
        </div>
        <RouterLink to="/about">ABOUT US</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style>
  @import '@/assets/base.css';
</style>
