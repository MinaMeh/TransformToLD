<template>
  <v-dialog v-model="active">
    <v-card>
      <v-card-title>search a property {{prop.property}}</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-text-field
              prepend-icon="mdi-magnify"
              label="Search"
              single-line
              v-model="search"
              hide-details
              class="mb-5"
            ></v-text-field>
            <v-btn @click="searchTerm()" class="mx-2" fab small color="blue">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>

            <v-col cols="12">
              <v-data-table :headers="headers" :items="properties" @click:row="test"></v-data-table>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="red darken-1" text @click="$emit('close')">Close</v-btn>
        <v-btn color="green darken-1" text @click="$emit('save')">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import axios from "axios";
export default {
  props: ["prop", "active"],
  data() {
    return {
      search: "",
      headers: [
        { text: "", value: "selected", align: "center" },
        { text: "Prefixed Name", value: "prefixedName" },
        { text: "URI", value: "uri" },
        { text: "Type", value: "type" },
        { text: "Score", value: "score" }
      ],
      properties: []
    };
  },
  methods: {
    searchTerm: function() {
      var formData = new FormData();
      formData.append("term", this.search);
      console.log(this.search);
      axios
        .post("http://127.0.0.1:8000/searchProperty/", formData)
        .then(response => {
          console.log(response.data);
          this.properties = response.data;
        })
        .catch(error => console.log(error));
    },
    test: function(value) {
      console.log(value);
      this.prop.result.push(value);
      this.prop.selected = value;
      this.$emit("close");
    }
  }
};
</script>