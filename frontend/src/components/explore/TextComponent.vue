<template>
  <v-container>
    <v-row class="mt-9">
      <h2 class="ml-5">Terms</h2>
      <v-col cols="12" v-for="prop in $store.state.text.paragraph.terms" :key="prop.uri">
        <v-card>
          <v-card-text>
            <v-row align="center" justify="center">
              <div cols="3" class="headline">{{prop.property}}</div>
              <v-col cols="8" class="ml-5">
                <v-select
                  class="property"
                  v-model="prop.selected"
                  label="Select a term"
                  :value="prop.selected.uri"
                  :items="prop.result"
                  item-value="uri"
                  :item-text="item => item.prefixedName +' - (score = '+ item.score+' )' +' - (term = '+ item.term+' )'"
                  return-object
                >
                  <template v-slot:selection="{ item }">
                    <a v-bind:href="item.uri" target="__">{{item.uri}}</a>
                  </template>
                </v-select>
              </v-col>
              <Modal
                v-if="modalVisible"
                @close="modalVisible = false"
                :prop="modalData"
                :active="modalVisible"
              ></Modal>
              <v-btn
                cols="1"
                color="blue"
                dark
                class="mx-2"
                fab
                small
                @click.stop="modalVisible = true"
                @click="openModal(prop)"
              >
                <v-icon dark>mdi-magnify</v-icon>
              </v-btn>
            </v-row>
          </v-card-text>
          <v-divider></v-divider>
        </v-card>
      </v-col>
      <h2 class="ml-5">Entities</h2>
      <v-col cols="12">
        <v-data-table :headers="headers" :items="$store.state.text.paragraph.entities">
          <template v-slot:item.uris="{ item }">
            <v-select label="select a term" v-model="item.selected" :items="item.uris">
              <template v-slot:selection="{ item }">
                <a v-bind:href="item" target="__">{{item}}</a>
              </template>
            </v-select>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <v-tour name="myTour" :steps="steps"></v-tour>
  </v-container>
</template>
<script>
import Modal from "@/Subcomponents/Modal.vue";

export default {
  components: {
    Modal
  },
  data() {
    return {
      tab: null,
      modalVisible: false,
      modalData: null,
      headers: [
        { text: "Entity", value: "text" },
        { text: "URI", value: "uris" }
      ],
      steps: [
        {
          target: ".property", // We're using document.querySelector() under the hood
          header: {
            title: "Map predicate"
          },
          content: `Map every predicate to its LOV term`,
          params: {
            enableScrolling: false
          }
        }
      ]
    };
  },
  computed: {
    guide() {
      return this.$store.state.guide;
    }
  },
  methods: {
    openModal(data) {
      console.log(data);
      this.modalData = data;
      this.modalVisible = true;
      console.log(this.modalVisible);
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
