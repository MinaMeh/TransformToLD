<template>
  <v-container class="mt-10">
    <v-row>
      <v-col cols="6" v-for="prop in terms" :key="prop.uri">
        <v-card>
          <v-card-text>
            <v-row align="center" justify="center">
              <v-col cols="4" class="ma-4 mt-8">
                <h4>{{prop.property}}</h4>
              </v-col>
              <v-col cols="8" class="ml-5">
                <v-select
                  label="Select a term"
                  :items="prop.result"
                  item-value="uri"
                  :item-text="item => item.prefixedName +' - (score = '+ item.score+' )' +' - (term = '+ item.term+' )'"
                  return-object
                ></v-select>
              </v-col>
            </v-row>
          </v-card-text>
          <v-divider></v-divider>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "CsvComponent",
  props: {
    terms: Array
  },
  data() {
    return {
      continue: true,
      properties: null
    };
  },
  watch: {
    count(newCount, oldCount) {
      console.log("old " + oldCount + " new count " + newCount);
      this.properties = this.$store.state.properties;
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
      return this.$store.state.csv.terms.length;
    }
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