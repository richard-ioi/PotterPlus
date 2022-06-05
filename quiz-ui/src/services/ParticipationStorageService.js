import QuizApiService from '../services/QuizApiService.js';

export default {
  clear() {
    return quizApiService.call("delete", "participations")
  },
  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
    //return quizApiService.call("post", "participations", )
  },
  getPlayerName() {
    return quizApiService.call("get", "participations")
  },
  saveParticipationScore(participationScore) {
    window.localStorage.setItem("score", participationScore)
  },

  //TODO : false 
  getParticipationScore() {
    console.log(quizApiService.getQuizInfo().score)
    return quizApiService.getQuizInfo().score
  },

};