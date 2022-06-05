<template>
  <img v-if="question.image" :src="question.image" />
  <p v-if="question.title">{{ question.title }} </p>
  <p v-if="question.text">{{ question.text }} </p>
  <a v-for="(answer, index) in question.possibleAnswers" :key="index" @click="$emit('answer-selected', index)">{{
  answer.text
  }}</a>
</template>
<script>
export default {
  props: {
    question: {
      type: Object
    },

  },
  emits: ["answer-selected"],
  async created() {
    console.log("Composant question display 'created'");
  }
}
</script>