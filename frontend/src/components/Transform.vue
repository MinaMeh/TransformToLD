<template>
  <v-container>
    <Navbar />
    <HorizontalStepper />
  </v-container>
</template>
<script>
import HorizontalStepper from "@/components/HorizontalStepper";
import Navbar from "@/components/Navbar";

export default {
  data() {
    return {
      snackbarCreate: false
    };
  },
  components: {
    HorizontalStepper,
    Navbar
  },
  methods: {
    test() {
      console.log("Hello");
    }
  }
};
</script>
