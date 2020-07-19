<template>
  <v-container class="mt-10">
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h2 id="preprocessing">Table columns</h2>
            <v-card-text>
              <v-simple-table>
                <thead>
                  <tr>
                    <th>Column</th>
                    <th>Translation</th>
                    <th>Possible values</th>
                  </tr>
                </thead>
                <tbody>
                  <tr></tr>
                  <tr v-for="header in headers" :key="header.name">
                    <td>{{header.name}}</td>
                    <td>{{header.translated}}</td>
                    <td>
                      <v-chip
                        class="ma-1"
                        color="primary"
                        v-for="comb in header.combinaison"
                        :key="comb"
                      >{{comb}}</v-chip>
                    </td>
                  </tr>
                </tbody>
              </v-simple-table>
            </v-card-text>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>
    <v-tour name="myTour" :steps="steps"></v-tour>
  </v-container>
</template>
<script>
export default {
  name: "CsvComponent",
  data() {
    return {
      continue: true,
      steps: [
        {
          target: "#preprocessing", // We're using document.querySelector() under the hood
          header: {
            title: "Confirm preprocessing"
          },
          content: `Confirm column translation and combinaisons`
        }
      ]
    };
  },
  computed: {
    headers() {
      var selected = [];
      this.$store.state.csv.headers.forEach(function(header) {
        if (header.selected) selected.push(header);
      });
      return selected;
    },
    guide() {
      return this.$store.state.guide;
    }
  },
  watch: {
    guide(newValue) {
      if (newValue == true) this.$tours["myTour"].start();
      else this.$tours["myTour"].stop();
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

  mounted() {
    if (this.$store.state.guide) this.$tours["myTour"].start();
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>