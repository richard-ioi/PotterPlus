<template>
<br>
  <h2>Your score :</h2> 
  <h2 v-if="score" >{{ score }}/10 </h2>
  <div class="one">
    <div width="500" height="400" ref="imgHouse" ></div> 
  </div> 
  <div ref="scoreDisplay" class="scoreDisplay">
    <img v-if="imgSrc" :src="imgSrc" style="object-fit: cover;display: block;  margin-left: auto;  margin-right: auto;  width: 50%;"/>
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
      playerPosition: 0,
      imgSrc: ''
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

    const houseTxt = this.$refs.housing;
    
    if (0 <= this.score <= 2) {
      houseTxt.innerHTML = "You're in Slytherin !";
      this.imgSrc ='https://upload.wikimedia.org/wikipedia/commons/3/34/Slytherin.png';
    }
    else if (3 <= this.score <= 5) {
      houseTxt.innerHTML = "You're in Hufflepuff !";
      this.imgSrc = 'https://www.nicepng.com/png/full/43-439104_hufflepuff-crest-harry-potter-banner-harry-potter-hufflepuff.png';
    }
    else if (6 <= this.score <= 8) {
      houseTxt.innerHTML = "You're in Gryffindor !";
      this.imgSrc = 'https://logolook.net/wp-content/uploads/2021/12/Gryffindor-Logo.png';
    }
    else if (9 <= this.score <= 10) {
      houseTxt.innerHTML = "You're in Ravenclaw !";
      this.imgSrc = 'https://www.pngmart.com/files/12/Ravenclaw-House-PNG-Clipart.png';
    } 
  }
};
</script>