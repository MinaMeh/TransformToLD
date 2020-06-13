<template>
  <v-container class="mt-10">
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h2>Table columns</h2>
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
  </v-container>
</template>
<script>
export default {
  name: "CsvComponent",
  data() {
    return {
      continue: true
    };
  },
  computed: {
    headers() {
      var selected = [];
      this.$store.state.csv.headers.forEach(function(header) {
        if (header.selected) selected.push(header);
      });
      return selected;
    }
  },
  watch: {
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
    this.content = this.$store.state.file_content;
    if (this.continue) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>