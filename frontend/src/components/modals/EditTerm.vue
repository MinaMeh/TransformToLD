<template>
  <v-dialog v-model="modal" max-width="400">
    <v-card>
      <v-card-title>Give the term URI</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            outlined
            label="Term URI"
            v-model="selectedTerm.term"
            prepend-icon="mdi-link"
          ></v-text-field>

          <v-btn color="error" @click="$emit('close')" class="mr-4">Cancel</v-btn>
          <v-btn color="success" @click="$emit('edit', selectedTerm)">OK</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  props: ["modal", "term"],
  data() {
    return {
      selectedTerm: { ...this.term }
    };
  }
};
</script>