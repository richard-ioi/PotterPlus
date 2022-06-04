<template>

  <head>
  </head>

  <body>
    <router-link to="/start-new-quiz-page" id=startBtn type="button" class="btn btn-primary">Démarrer le quiz !
    </router-link>
    <table id=bestScores class="table table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Prénom</th>
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
  </body>

</template>

<script>
import QuizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: []
    };
  },
  async created() {
    var quizInfoApiResult = await QuizApiService.getQuizInfo();
    this.registeredScores = quizInfoApiResult.data.scores;
    console.log("Composant Home page 'created'");
    console.log("Registered Scores: ", this.registeredScores);
  }
};
</script>