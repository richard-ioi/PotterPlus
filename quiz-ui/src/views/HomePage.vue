<template>
  <head>
  </head>
  <body>
    <button id = startBtn type="button" class="btn btn-primary" >Start the quiz</button>
    <table id =  bestScores class="table table-striped" >
      <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">First</th>
        <th scope="col">Last</th>
        <th scope="col">Handle</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row">1</th>
        <td>Mark</td>
        <td>Otto</td>
        <td>@mdo</td>
      </tr>
      <tr>
        <th scope="row">2</th>
        <td>Jacob</td>
        <td>Thornton</td>
        <td>@fat</td>
      </tr>
      <tr>
        <th scope="row">3</th>
        <td>Larry</td>
        <td>the Bird</td>
        <td>@twitter</td>
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