<template>
  <v-container class="mt-10">
    <v-form class="px-3">
      <v-text-field
        outlined
        label="Dataset Title"
        v-model="$store.state.metadata.title"
        placeholder="Enter the title of your dataset"
        prepend-icon="mdi-file"
      ></v-text-field>

      <v-text-field
        outlined
        label="Creator"
        v-model="$store.state.metadata.creator"
        placeholder="Enter creator of your dataset"
        prepend-icon="mdi-file"
      ></v-text-field>
      <v-text-field
        outlined
        label="License"
        v-model="$store.state.metadata.license"
        prepend-icon="mdi-file"
      ></v-text-field>
      <v-text-field
        outlined
        label="Subject"
        v-model="$store.state.metadata.subject"
        prepend-icon="mdi-file"
      ></v-text-field>
      <v-textarea
        counter
        outlined
        label="Description of your dataset"
        v-model="$store.state.description"
        placeholder="Describe your data set"
        prepend-icon="mdi-file-document-edit"
      ></v-textarea>
    </v-form>
  </v-container>
</template>
<script>
export default {
  data() {
    return {
      continue: true
    };
  },

  mounted() {
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>
