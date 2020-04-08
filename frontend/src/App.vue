<template>
  <v-app>
    <v-content>
      <HorizontalStepper />
    </v-content>
  </v-app>
</template>

<script>
import HorizontalStepper from "./components/HorizontalStepper";

export default {
  name: "App",

  components: {
    HorizontalStepper
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