import quizApiService from "@/services/QuizApiService";

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
    //return quizApiService.call("post", "participations", participationScore)
  },
  getParticipationScore() {
    console.log(quizApiService.getQuizInfo().score)
    return quizApiService.getQuizInfo().score
  }
};