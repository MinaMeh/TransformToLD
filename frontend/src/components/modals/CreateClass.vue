<template>
  <v-dialog v-model="active" max-width="600">
    <v-card>
      <v-card-title>Create A class</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                outlined
                prepend-icon="mdi-label"
                label="rdfs:label"
                single-line
                v-model="label"
                hide-details
                class="mb-5"
              ></v-text-field>
              <v-text-field
                outlined
                prepend-icon="mdi-arrow-up"
                label="rdfs:subClassOf (optional)"
                single-line
                v-model="subClassOf"
                hide-details
                class="mb-5"
              ></v-text-field>
              <v-textarea
                outlined
                prepend-icon="mdi-comment-text"
                label="rdfs:comment"
                single-line
                v-model="comment"
                hide-details
                class="textareamb-5"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="red darken-1" text @click="$emit('close')">Close</v-btn>
        <v-btn color="green darken-1" text @click="create">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import instance from "@/services/MainService";
export default {
  props: ["active"],
  data() {
    return {
      label: "",
      comment: "",
      subClassOf: "",
      properties: []
    };
  },
  methods: {
    create: function() {
      console.log("hereh");
      var formData = new FormData();
      var Rdfclass = {
        comment: this.comment,
        label: this.label,
        subClassOf: this.subClassOf
      };
      formData.append("project_id", this.$store.state.project_id);
      formData.append("class", JSON.stringify(Rdfclass));
      console.log("before send", Rdfclass);
      instance
        .post("createClass/", formData)
        .then(response => {
          console.log(response.data);
          this.$emit("closeClass", response.data);
        })
        .catch(error => console.log(error.response));
    }
  }
};
</script>