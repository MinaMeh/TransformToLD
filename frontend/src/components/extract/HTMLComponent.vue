<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="mt-8">
        <v-card>
          <v-card-title>
            <h2>File Statistics</h2>
          </v-card-title>
          <v-card-text>
            <v-col cols="5">
              <v-simple-table>
                <tr>
                  <th>File size</th>
                  <td>{{$store.state.size}}</td>
                </tr>
                <tr>
                  <th>Number of tables</th>
                  <td>{{$store.state.html.num_tables}}</td>
                </tr>
                <tr>
                  <th>Number of paragraphs</th>
                  <td>{{$store.state.html.num_paragraphs}}</td>
                </tr>
              </v-simple-table>
            </v-col>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-tabs class="mt-8" v-model="tab">
      <v-tab>Tables</v-tab>
      <v-tab>Paragraphs</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-col cols="12">
          <v-card v-for="table in $store.state.html.tables" :key="table.id" class="mt-3">
            <v-card-title>
              <v-checkbox
                v-model="table.selected"
                :id="String(table.id)"
                :value="table.id"
                class="mt-10"
              ></v-checkbox>
              <h2>Table #{{table.id}}</h2>
            </v-card-title>
            <v-card-text>
              <v-col cols="3">
                <h3>Table Statistics</h3>
                <v-simple-table dense>
                  <tr>
                    <th>Number of lines</th>
                    <td>{{table.lines}}</td>
                  </tr>
                  <tr>
                    <th>Number of columns</th>
                    <td>{{table.columns}}</td>
                  </tr>
                </v-simple-table>
              </v-col>
              <v-col col="9">
                <v-simple-table dense class="mt-5">
                  <thead>
                    <tr>
                      <th></th>
                      <th>Column</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(header,index) in table.headers" :key="index">
                      <td>
                        <v-checkbox
                          v-model="header.selected"
                          :disabled="!table.selected"
                          @change="toggleCol(header,table.id)"
                          :id="String(header)"
                          :value="header.name"
                        ></v-checkbox>
                      </td>
                      <td>{{header.name}}</td>
                    </tr>
                  </tbody>
                </v-simple-table>
              </v-col>
            </v-card-text>
          </v-card>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col
          cols="12"
          v-for="(paragraph,index) in $store.state.html.paragraphs"
          :key="index"
          class="mt-3"
        >
          <Paragraphs :paragraph="paragraph.paragraph" :sentences="paragraph.sentences" :id="index"></Paragraphs>
        </v-col>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>
<script>
import Paragraphs from "@/Subcomponents/Paragraphs";

export default {
  name: "HTMLComponent",
  components: {
    Paragraphs
  },
  data() {
    return {
      tab: null,
      continue: true,
      selected: "",
      tables_selected: [],
      content: null
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
  methods: {
    tableContainsHeader: function(table_id, header) {
      var existe = false;
      var tables = this.$store.state.html.tables_selected.filter(table => {
        return table.id == table_id;
      });
      var contain = tables[0].columns_selected.filter(col => {
        return col == header;
      });
      if (contain.length != 0) existe = true;
      console.log("existe", existe);
      return existe;
    },
    tableIsNotSelected: function(table_id) {
      var not_selected = true;
      var tables = this.$store.state.html.tables_selected.filter(table => {
        return table.id == table_id;
      });
      if (tables && tables.length) not_selected = false;
      return not_selected;
    },
    toggleTable: function(table_id) {
      console.log(table_id);
      var tables = this.$store.state.html.tables_selected.filter(table => {
        return table.id == table_id;
      });
      console.log("len(tables)" + tables.length);

      if (tables && tables.length) {
        this.$store.state.html.tables_selected.splice(tables[0], 1);
      } else {
        this.$store.state.html.tables_selected.push({
          id: table_id,
          columns_selected: []
        });
      }
      console.log(this.$store.state.html.tables_selected);
    },
    toggleCol: function(header, table_id) {
      var tables = this.$store.state.html.tables_selected.filter(table => {
        return table.id == table_id;
      });
      var contain = tables[0].columns_selected.filter(col => {
        return col == header;
      });
      if (contain.length == 0) tables[0].columns_selected.push(header);
      else tables[0].columns_selected.splice(header, 1);
      console.log(header, table_id);
      console.log(this.$store.state.html.tables_selected);
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