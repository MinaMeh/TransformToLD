<template>
  <v-app class="bg">
    <v-container class="mx-auto">
      <v-row>
        <v-col md="6" sm="10" offset-md="3" class="mt-10">
          <v-col md="10" offset="1">
            <v-card color="rgba(255, 255, 240, 0.8)">
              <v-card-text>
                <v-col cols="8" offset="4">
                  <img src="/logo-sm.png" alt="Logo" />
                </v-col>
                <v-col md="10" sm="12" offset-md="1">
                  <v-form>
                    <v-text-field
                      outlined
                      placeholder="Email"
                      v-model="userData.email"
                      prepend-inner-icon="mdi-email"
                    ></v-text-field>
                    <v-text-field
                      outlined
                      placeholder="password"
                      v-model="userData.password"
                      prepend-inner-icon="mdi-lock"
                    ></v-text-field>You don't have an account?
                    <router-link to="/signup">Sign Up</router-link>
                    <br />
                    <v-col cols="2" offset="8">
                      <v-btn color="success" @click.prevent="login">Login</v-btn>
                    </v-col>
                  </v-form>
                </v-col>
              </v-card-text>
            </v-card>
          </v-col>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>
<script>
export default {
  data() {
    return {
      userData: {
        email: "",
        password: ""
      }
    };
  },
  methods: {
    login() {
      this.$store
        .dispatch("userLogin", {
          email: this.userData.email,
          password: this.userData.password
        })
        .then(() => {
          console.log("test");
          this.$router.push({ name: "home" });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>
<style scoped>
.bg {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  background: url("/bg.jpg") no-repeat center center;
  background-size: cover;
  transform: scale(1.1);
}
</style>