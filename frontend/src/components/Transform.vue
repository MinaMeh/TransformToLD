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
  components: {
    HorizontalStepper,
    Navbar
  }
};
</script>