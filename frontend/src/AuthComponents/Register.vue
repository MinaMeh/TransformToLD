<template>
  <v-app class="bg">
    <v-container>
      <v-row>
        <v-col md="6" sm="10" offset-md="3">
          <v-col md="10" offset="1">
            <v-card color="rgba(255, 255, 240, 0.8)">
              <v-card-title>
                <v-col cols="8" offset="4">
                  <img src="/logo-sm.png" alt="Logo" />
                </v-col>
              </v-card-title>
              <v-card-text>
                <v-col md="10" sm="12" offset-md="1">
                  <v-form>
                    <v-text-field
                      outlined
                      placeholder="First Name"
                      v-model="userData.first_name"
                      prepend-inner-icon="mdi-account"
                    ></v-text-field>
                    <v-text-field
                      outlined
                      placeholder="Last Name"
                      v-model="userData.last_name"
                      prepend-inner-icon="mdi-account"
                    ></v-text-field>
                    <v-text-field
                      outlined
                      placeholder="email"
                      v-model="userData.email"
                      prepend-inner-icon="mdi-email
"
                    ></v-text-field>

                    <v-text-field
                      outlined
                      placeholder="password"
                      v-model="userData.password"
                      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                      @click:append="show1 = !show1"
                      :type="show1 ? 'text' : 'password'"
                      prepend-inner-icon="mdi-lock"
                    ></v-text-field>
                    <v-col cols="2" offset="8">
                      <v-btn color="success" left @click.prevent="signup"
                        >Sign Up</v-btn
                      >
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
      show1: false,
      userData: {
        email: "",
        first_name: "",
        last_name: "",
        password: "",
      },
    };
  },
  methods: {
    signup() {
      this.$store
        .dispatch("userRegister", {
          email: this.userData.email,
          password: this.userData.password,
          first_name: this.userData.first_name,
          last_name: this.userData.last_name,
        })
        .then(() => {
          console.log("test");
          this.$router.push({ name: "home" });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
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
