<template>
  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
</template>
<script>
import QuestionDisplayVue from './QuestionDisplay.vue'
import QuizApiService from '@/services/QuizApiServices';
export default {
  components: {
    QuestionDisplayVue
  },

  data() {
    return {
      currentPosition: 0,
      question: null,
      answersSummaries: [],
      questionCount: 0,
    }
  },

  async created() {
    console.log("Composant question page 'created'");
    await this.loadQuestionByPosition()
  },
  methods: {
    async loadQuestionByPosition() {
      const { data } = await QuizApiService.getQuestion(this.currentPosition)
      this.question = data
      this.questionCount = 10 //TODO question count function.
    },
    async answerClickedHandler() { },
    async endQuiz() { }
  }

}

</script>
<style>
</style>