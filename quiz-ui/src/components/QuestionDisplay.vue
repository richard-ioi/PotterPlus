<template>
  <div class="wrapper2">
    <div class="one">
      <img v-if="question.image" :src="question.image" width="500" height="400"/>
    </div>  
    <div class="two">
      <h3 v-if="question.title">{{ question.title }} </h3>
      <h2 v-if="question.text">{{ question.text }} </h2>
      <a v-for="(answer, index) in question.possibleAnswers" :key="index" @click="$emit('answer-selected', index)">
        <button class="btn btn-outline-light" style="width:400px">{{answer.text}} </button> <br><br>
      </a>
    </div>
  </div> 
</template>
<script>
export default {
  props: {
    question: {
      type: Object
    },

  },
  emits: ["answer-selected"],
  async created() {
    console.log("Composant question display 'created'");
  }
}
</script>