
<template>
  <v-container class="mt-10">
    <v-row>
      <v-col col="12">
        <v-card>
          <v-card-title>
            <h2>Statistics</h2>
          </v-card-title>
          <v-card-text>
            <v-simple-table dense>
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
              <v-data-table dense :headers="headers" :items="$store.state.csv.headers">
                <template v-slot:item="header">
                  <tr>
                    <td>
                      <v-checkbox
                        class="columns mt-3"
                        v-model="header.item.selected"
                        :id="String(header.item.name)"
                        :value="header.item.selected"
                      ></v-checkbox>
                    </td>
                    <td>
                      <div class="mt-5">
                        <v-edit-dialog
                          :return-value.sync="header.item.name"
                          lazy
                          @save="save"
                          @cancel="cancel"
                          @open="open"
                          @close="close"
                        >
                          {{ header.item.name }}
                          <template v-slot:input>
                            <v-text-field
                              v-model="header.item.name"
                              label="Edit"
                              single-line
                              counter
                            ></v-text-field>
                          </template>
                        </v-edit-dialog>
                      </div>
                    </td>
                    <td>
                      <v-select class="type" :items="datatypes" v-model="header.item.type"></v-select>
                    </td>
                  </tr>
                </template>
              </v-data-table>
              <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                {{ snackText }}
                <v-btn text @click="snack = false">Close</v-btn>
              </v-snackbar>
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
  data() {
    return {
      continue: true,
      snack: false,
      snackColor: "",
      snackText: "",

      headers: [
        { text: "Add", value: "Add" },
        { text: "Header", value: "name", sortable: false },
        { type: "Data Type", value: "type" }
      ],
      datatypes: [
        "xsd:int",
        "xsd:float",
        "xsd:string",
        "xsd:boolean",
        "xsd:date"
      ],
      steps: [
        {
          target: ".columns", // We're using document.querySelector() under the hood
          header: {
            title: "Select columns"
          },
          content: `Select columns that you want to include in the conversion`
        },
        {
          target: ".type",
          content: "Select column type!"
        }
      ]
    };
  },
  computed: {
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
  methods: {
    save() {
      this.snack = true;
      this.snackColor = "success";
      this.snackText = "Data saved";
    },
    cancel() {
      this.snack = true;
      this.snackColor = "error";
      this.snackText = "Canceled";
    },
    open() {
      this.snack = true;
      this.snackColor = "info";
      this.snackText = "Edit header name";
    },
    close() {
      console.log("Dialog closed");
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