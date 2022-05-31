<template>
  <h1>Quiz page</h1>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "NewQuizPage",
  data() {
    return {
    };
  },
  async created() {
    console.log("Composant New Quiz Page 'created'");
  }
};
</script>