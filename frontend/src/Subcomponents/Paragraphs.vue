<template>
  <v-container class="mt-8">
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h2>Text</h2>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <h4 class="text-center">Sentences</h4>
                <v-data-table :headers="headers" :items="sentences">
                  <template v-slot:item.id="{item}">#{{sentences.indexOf(item)+1}}</template>
                </v-data-table>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  props: {
    sentences: Array
  },
  data() {
    return {
      paragraphs: null,
      queries: [],
      headers: [
        { text: "id", value: "id" },

        { text: "Sentence", value: "text" }
      ]
    };
  },
  methods: {
    getTagsNames(tags) {
      var names = [];
      for (var tag in tags) {
        names.push(tags[tag].word);
      }
      console.log(names);
      return names;
    }
  },
  mounted() {
    for (var word in this.tags) {
      this.queries.push(this.tags[word].name);
    }
  }
};
</script>