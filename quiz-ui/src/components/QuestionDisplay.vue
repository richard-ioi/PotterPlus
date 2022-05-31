<template>
  <img v-if="question.image" :src="question.image" />
  <a @click="$emit('answer-selected', 2)">La réponse D</a>
</template>
<script>
  export default {
    props: {
      question: {
        type: Object
      },
      emits: ["answer-selected"]
    }
  }
</script>