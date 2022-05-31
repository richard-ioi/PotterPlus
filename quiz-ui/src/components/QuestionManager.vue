<template>
  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
</template>
<script>
import QuestionDisplayVue from './icons/QuestionDisplay.vue'
export default {
  components: {
    QuestionDisplayVue
  },
  props: {

  },
  async created() {
    console.log("Composant Home page 'created'");
  },
  async loadQuestionByPosition() { },
  async answerClickedHandler() { },
  async endQuiz() { }
}

</script>