<template>
  <v-app>
    <v-content>
    <Navbar/>
    <HorizontalStepper />
    </v-content>
  </v-app>
</template>

<script>
import HorizontalStepper from "./components/HorizontalStepper";
import Navbar from "./components/Navbar";
export default {
  name: "App",

  components: {
    HorizontalStepper,
    Navbar
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