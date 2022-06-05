<template>

  <head>
  </head>

  <body>
    <div class="container">
      <div class="center">
        <router-link to="/start-new-quiz-page" id=startBtn type="button" class="btn-sample badge" >Start the quiz !</router-link>
      </div>
    </div>
    
    <div class="container">
      <h3>All player's scores</h3>
      <table id=bestScores class="table table-hover">
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