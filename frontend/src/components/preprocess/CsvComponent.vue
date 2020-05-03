<template>
  <v-container class="mt-10">
    <v-row>
      <v-col col="12">
        <v-card>
          <v-card-title>
            <h2>Statistics</h2>
          </v-card-title>
          <v-card-text>
            <v-simple-table>
              <tr>
                <th>Size of the file</th>
                <td>{{content.size}} Bytes</td>
              </tr>

              <tr>
                <th>Number of lines</th>
                <td>{{content.results.lines}}</td>
              </tr>
              <tr>
                <th>Number of columns</th>
                <td>{{content.results.columns}}</td>
              </tr>
            </v-simple-table>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <h2>Table columns</h2>
            <v-card-text>
              <v-simple-table>
                <thead>
                  <tr>
                    <th></th>
                    <th>Column</th>
                    <th>Translation</th>
                    <th>Possible values</th>
                  </tr>
                </thead>
                <tbody>
                  <tr></tr>
                  <tr v-for="header in content.results.headers" :key="header.header">
                    <td>
                      <v-checkbox v-model="columns_selected" :id="header.name" :value="header.name"></v-checkbox>
                    </td>

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
      continue: true,
      content: null,
      columns_selected: []
    };
  },
  watch: {
    count(newCount, oldCount) {
      console.log("old " + oldCount + " new count " + newCount);
      this.content = this.$store.state.file_content;
    },
    columns(newCols, oldCols) {
      console.log("old " + oldCols + " new  " + newCols[0]);
      this.$store.state.csv.columns = this.columns_selected;
      console.log("store " + typeof Array(this.columns_selected));
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
    count() {
      return this.$store.state.file_content.length;
    },
    columns() {
      return this.columns_selected;
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