<template>
<br>
  <h2>Your score :</h2> 
  <h2 v-if="score" >{{ score }}/10 </h2>
  <div ref="scoreDisplay" class="scoreDisplay">
    <h2 ref="housing" ></h2>
  </div>
  <br>
  <router-link to="/" id=startBtn type="button" class="btn btn-outline-light" style="display:inline;  position: relative; float:right;">
    Retour à l'écran d'accueil principal !
  </router-link><br><br>
  <p style="display:inline">You can check yours and others players' ranking</p>
  
  
  <div class="container">
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


    if (0 <= this.score <= 2) {
      this.$refs.housing.innerHTML = "You're in Slytherin !";
      this.$refs.scoreDisplay.style.background = "#16680ba8";
    }
    else if (3 <= this.score <= 5) {
      this.housing.innerHTML = "You're in Hufflepuff !";
      this.$refs.scoreDisplay.style.background = "#b8a927a8";
    }
    else if (6 <= this.score <= 8) {
      this.$refs.housing.innerHTML = "You're in Gryffindor !";
      this.$refs.scoreDisplay.style.background = "#af2b26a8";
    }
    else if (9 <= this.score <= 10) {
      this.$refs.housing.innerHTML = "You're in Ravenclaw !";
      this.$refs.scoreDisplay.style.background = "#233897a8";
    } 
  }
};
</script>