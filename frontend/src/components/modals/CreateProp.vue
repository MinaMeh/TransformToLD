<template>
  <v-dialog v-model="active" max-width="600">
    <v-card>
      <v-card-title>Create A property for {{prop.property}}</v-card-title>
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
                label="rdfs:subPropertyOf (optional)"
                single-line
                v-model="subPropertyOf"
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
  props: ["prop", "active"],
  data() {
    return {
      label: "",
      comment: "",
      subPropertyOf: "",
      properties: []
    };
  },
  methods: {
    create: function(value) {
      console.log("hereh");
      var formData = new FormData();
      var prop = {
        comment: this.comment,
        label: this.label,
        subPropertyOf: this.subPropertyOf
      };
      formData.append("project_id", this.$store.state.project_id);
      formData.append("prop", JSON.stringify(prop));
      console.log("before send", prop);
      instance
        .post("createProperty/", formData)
        .then(response => {
          console.log(response.data);
          console.log(value);
          this.prop.result.push(response.data);
          this.prop.selected = response.data;
          console.log("this prop selected", this.prop.selected);
          this.$emit("close");
        })
        .catch(error => console.log(error.response));
    }
  }
};
</script>