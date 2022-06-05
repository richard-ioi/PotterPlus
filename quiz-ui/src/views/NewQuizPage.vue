<template>
  <head>
  </head>
  <body>
    <div class="wrapper2">
      <div class="one">
        <br>
        <h2>Are you ready to take a new Quiz ? </h2>
        <br>
        <p>But first, enter your name :</p>
        <input v-model="username" type="text" name="name" size="10">
        <p>{{ username }}</p>
        <btn class="btn-sample badge" @click="launchNewQuiz"  style="text-align:center">Start</btn>
      </div>
    </div>
    </body>
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