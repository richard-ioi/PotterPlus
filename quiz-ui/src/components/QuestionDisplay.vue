<template>
  <img v-if="question.image" :src="question.image" />
  <p v-if="question.title" :src="question.title"> </p>
  <p v-if="question.text" :src="question.text"> </p>
  <a v-for="(answer, index) in question.possibleAnswers" :key="index" @click="$emit('answer-selected', index)">{{ answer
  }}></a>
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