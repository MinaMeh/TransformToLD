<template>
  <v-dialog v-model="chooseOutput" max-width="400">
    <v-card>
      <v-card-title>Choose output file format</v-card-title>
      <v-card-text>
        <v-form>
          <v-select
            outlined
            v-model="selectedFormat"
            label="Select an output format"
            :items="outputFormat"
            item-value="value"
            item-text="text"
          ></v-select>
          <v-btn color="error" @click="$emit('close')" class="mr-4">Cancel</v-btn>
          <v-btn color="success" @click="$emit('convert', selectedFormat)">OK</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  props: ["chooseOutput"],
  data() {
    return {
      outputFormat: [
        { text: "Turtle", value: "turtle" },
        { text: "XML", value: "xml" },
        { text: "JSON-LD", value: "json-ld" },
        { text: "N3", value: "n3" },
        { text: "NT", value: "nt" },
        { text: "NQUADS", value: "nquads" },
        { text: "Trix", value: "trix" },
        { text: "Trig", value: "trig" },
      ],
      selectedFormat: "",
    };
  },
};
</script>