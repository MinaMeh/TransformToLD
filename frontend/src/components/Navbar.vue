<template>
  <nav>
    <v-snackbar v-model="snackbar" :timeout="4000" top color="success">
      <span>a new project has been created</span>
      <v-btn text color="white" @click="snackbar = false">Close</v-btn>
      <v-icon class="white--text">mdi-close-thick</v-icon>
    </v-snackbar>

    <v-app-bar app flat color="#3493b3ff">
      <v-app-bar-nav-icon @click.stop="sidebarMenu = !sidebarMenu" class="white--text"></v-app-bar-nav-icon>
      <v-toolbar-title class="white--text">Data Linked</v-toolbar-title>
      <v-divider class="mx-4" inset vertical></v-divider>
      <v-spacer></v-spacer>
      <v-btn text color="white" @click.prevent="logout">Logout</v-btn>
      <v-icon class="white--text">mdi-account</v-icon>
    </v-app-bar>
    <v-navigation-drawer
      v-model="sidebarMenu"
      app
      floating
      :permanent="sidebarMenu"
      :mini-variant.sync="mini"
      color="grey lighten-4"
    >
      <v-layout column align-center>
        <v-list-item class="px-2" @click="toggleMini = !toggleMini">
          <v-flex class="mt-4">
            <img :aspect-ratio="16/9" src="/logo-sm.png" alt="Logo" />
          </v-flex>
          <v-btn icon small>
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>
      </v-layout>
      <v-list-item>
        <v-list-item-icon>
          <v-icon>mdi-account-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-content class="text-truncate">User name</v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list>
        <v-list-item-group color="#3493b3ff">
          <v-list-item v-for="item in items" :key="item.title" link :to="item.href">
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      sidebarMenu: true,
      toggleMini: false,
      snackbar: false,
      items: [
        { title: "Home", href: "", icon: "mdi-home-outline" },
        { title: "Historical", href: "", icon: "mdi-palette-swatch" }
      ]
    };
  },
  methods: {
    logout() {
      this.$store
        .dispatch("userLogout")
        .then(this.$router.push({ name: "login" }));
    }
  },
  computed: {
    mini() {
      return this.$vuetify.breakpoint.smAndDown || this.toggleMini;
    }
  }
};
</script>
