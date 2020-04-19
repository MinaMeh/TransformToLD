<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h2>Text</h2>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" class="mb-5">
                <text-highlight
                  :queries="queries"
                  highlightStyle="background-color: #1E88E5; color:white"
                >{{results.text}}</text-highlight>
              </v-col>
              <v-col cols="12">
                <v-card>
                  <v-card-text>
                    <h4 class="text-center">Entities</h4>
                    <v-data-table
                      dense
                      :headers="headers"
                      :items="results.entities"
                      show-select
                      item-key="name"
                      v-model="selected"
                    >
                      <template v-slot:item.Entity="item">{{item.item.name}}</template>
                      <template v-slot:item.Class="item">
                        <v-chip color="primary">{{item.item.entity_type}}</v-chip>
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
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
  data() {
    return {
      headers: [
        { text: "Entity", value: "Entity" },
        { text: "Class", value: "Class" }
      ],
      results: null,
      queries: ["text"]
    };
  },
  watch: {
    type(newType, oldType) {
      console.log("old " + oldType + " new type " + newType);
      this.results = this.$store.state.file_content.results;
      console.log("queries" + this.queries);
      console.log(this.results.entities);
      //this.queries = this.results.entities;
    },
    $v: {
      handler: function() {
        if (this.continue) {
          this.$emit("can-continue", { value: true });
        } else {
          this.$emit("can-continue", { value: false });
        }
      },
      deep: true
    }
  },
  computed: {
    type() {
      return this.$store.state.file_content.type;
    }
  },
  mounted() {
    this.results = this.$store.state.file_content.results;
    for (var word in this.results.entities) {
      this.queries.push(this.results.entities[word].name);
    }

    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>