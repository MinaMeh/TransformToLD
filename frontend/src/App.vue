<template>
  <v-app>
    <v-content>
      <Navbar />
      <!-- <Home />-->
      <HorizontalStepper />
    </v-content>
  </v-app>
</template>

<script>
import HorizontalStepper from "./components/HorizontalStepper";
import Navbar from "./components/Navbar";
//import Home from "./components/Home";
export default {
  name: "App",

  components: {
    HorizontalStepper,
    Navbar
    // Home
  },

  data: () => ({
    //
  })
};
</script>
<style>
.v-application {
  font-family: sans-serif !important;
}
</style>