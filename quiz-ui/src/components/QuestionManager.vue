<template>
  <br>
  <h1>Question {{ currentPosition }} / {{ totalNumberOfQuestion }}</h1>
  <br>
  <QuestionDisplay :question="currentQuestion" v-if="currentQuestion" @answer-selected="answerClickedHandler" />
</template>
<script>

import QuestionDisplay from './QuestionDisplay.vue'
import QuizApiService from '../services/QuizApiService.js';
import ParticipationStorageService from '../services/ParticipationStorageService';

export default {
  components: {
    QuestionDisplay
  },

  data() {
    return {
      currentPosition: 1,
      currentQuestion: {
        title: '',
        text: '',
        image: '',
        position: 0,
        possibleAnswers: null,
      },
      answersSummaries: [],
      totalNumberOfQuestion: 0,
    }
  },

  async created() {
    console.log("Composant question page 'created'");
    await this.loadQuestionByPosition();
    await this.getQuizSize();
  },
  methods: {
    async loadQuestionByPosition() {
      console.log(this.currentQuestion)
      const { data } = await QuizApiService.getQuestion(this.currentPosition);
      this.currentQuestion = data
      //this.totalNumberOfQuestion = 10; //TODO question count function.
      //return this.question;
    },

    async answerClickedHandler(index) {
      if (this.currentPosition < this.totalNumberOfQuestion) {
        this.currentPosition++;
        this.answersSummaries.push(index + 1);
        console.log(this.answersSummaries);
        await this.loadQuestionByPosition();
      }
      else {
        this.answersSummaries.push(index + 1);
        const getScore = await this.getScore();
        const score = getScore.data.score
        console.log("SCORE", score);
        ParticipationStorageService.saveParticipationScore(score);
        this.endQuiz();
      }

    },
    async endQuiz() {
      this.$router.push('/score');
    },
    async getScore() {
      return await QuizApiService.saveParticipation(window.localStorage.getItem('playerName'), this.answersSummaries);
    },
    async getQuizSize() {
      const quizInfo = await QuizApiService.getQuizInfo();
      this.totalNumberOfQuestion = quizInfo.data.size;
    }
  }

}

</script>
<style>
</style>