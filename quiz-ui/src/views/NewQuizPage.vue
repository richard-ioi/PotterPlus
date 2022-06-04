<template>
  <h1>Start New Quiz</h1>
  <br>
  <p>Entrez votre nom :</p>
  <br>
  <input v-model="username" type="text" name="name" size="10">
  <p>{{ username }}</p>
  <br>
  <button @click="launchNewQuiz">GO!</button>
</template>

<script>
import participationStorageService from "../services/ParticipationStorageService";
export default {
  name: "NewQuizPage",
  data() {
    return {
      username: '',
    }
  },
  async created() {
    console.log("Composant New Quiz Page 'created'");
  },
  methods: {
    launchNewQuiz() {
      console.log("Launch new quiz with", this.username);
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    },
  }
};
</script>