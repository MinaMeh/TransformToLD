<template>
  <v-container class="mt-8">
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h2>Paragraph #{{id}}</h2>
          </v-card-title>
          <v-card-text>
            <v-row>{{paragraph}}</v-row>
            <v-row>
              <v-col cols="12">
                <h4 class="text-center">Sentences</h4>
                <v-expansion-panels>
                  <v-expansion-panel v-for="(sentence,i) in sentences" :key="i">
                    <v-expansion-panel-header>{{sentence}}</v-expansion-panel-header>
                    <v-expansion-panel-content></v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
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
    sentences: Array,
    tags: Array,
    id: Number,
    paragraph: String
  },
  data() {
    return {
      paragraphs: null,
      queries: [],
      headers: [
        { text: "Entity", value: "Entity" },
        { text: "Class", value: "Class" }
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