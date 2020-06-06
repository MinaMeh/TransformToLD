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
                <td>{{$store.state.size}} Bytes</td>
              </tr>

              <tr>
                <th>Number of lines</th>
                <td>{{$store.state.csv.lines}}</td>
              </tr>
              <tr>
                <th>Number of columns</th>
                <td>{{$store.state.csv.columns}}</td>
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
                  </tr>
                </thead>
                <tbody>
                  <tr></tr>
                  <tr v-for="(header,index) in $store.state.csv.headers" :key="index">
                    <td>
                      <v-checkbox v-model="header.selected" :id="header" :value="header.selected"></v-checkbox>
                    </td>

                    <td>
                      <div class="mt-4 headline">{{header.name}}</div>
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
  data() {
    return {
      continue: true
    };
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
  computed: {},
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