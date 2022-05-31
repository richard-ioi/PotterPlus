<template>
  <h1>Home page</h1>
</template>

<script>
  import QuizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores : []
    };
  },
  async created() {
    this.registeredScores = QuizApiService.getQuizInfo();
		console.log("Composant Home page 'created'");
    console.log("Registered Scores: ", this.registeredScores);
  }
};
</script>