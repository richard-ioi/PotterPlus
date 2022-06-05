<template>
  <div>SCORES</div>
  <p v-if="score">{{ score }} </p><br>
  <router-link to="/" id=startBtn type="button" class="btn btn-outline-light">Retour à l'écran d'accueil principal !
  </router-link><br>
  <div class="container">
    <h3>All player's scores</h3>
    <table id=bestScores class="table table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Name</th>
          <th scope="col">Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(scoreEntry, index) in this.registeredScores" v-bind:key="scoreEntry.date">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ scoreEntry.playerName }}</td>
          <td>{{ scoreEntry.score }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import QuizApiService from "@/services/QuizApiService";
export default {
  name: "ScorePage",
  data() {
    return {
      playerName: '',
      score: 0,
      registeredScores: [],
      playerPosition: 0
    };
  },
  async created() {
    //Gets playerName and score stored in localStorage by QuestionManager
    this.playerName = window.localStorage.getItem('playerName');
    this.score = window.localStorage.getItem('score');

    //Gets the QuizInfo used for the best scores array
    var quizInfoApiResult = await QuizApiService.getQuizInfo();
    this.registeredScores = quizInfoApiResult.data.scores;
    console.log("Composant ScorePage 'created'");
    console.log("Registered Scores: ", this.registeredScores);
  }
};
</script>