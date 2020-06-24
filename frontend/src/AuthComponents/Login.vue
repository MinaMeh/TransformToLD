  
<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="8">
        <v-card class="elevation-12">
          <v-window v-model="step">
            <v-window-item :value="1">
              <v-row>
                <v-col cols="12" md="8">
                  <v-card-text class="mt-6">
                    <h1
                      class="mb-4 text-center font-weight-bold display-2 primary--text text--accent-4"
                    >Sign In DataLinked !</h1>
                    <v-divider></v-divider>

                    <v-form>
                      <v-text-field
                        label="Email"
                        name="Email"
                        v-model="userDataLogin.email"
                        prepend-icon="mdi-email"
                        type="text"
                        color="primary accent-4"
                      />
                      <v-text-field
                        id="password"
                        label="Password"
                        name="Password"
                        v-model="userDataLogin.password"
                        prepend-icon="mdi-lock"
                        type="password"
                        color="primary accent-4"
                      />
                    </v-form>
                    <h3 class="text-right mt-3">Forget your password ?</h3>
                  </v-card-text>
                  <div class="text-center mt-3 mb-3">
                    <v-btn color="primary accent-4" dark @click.prevent="login">SIGN IN</v-btn>
                  </div>
                </v-col>
                <v-col cols="12" md="4" class="primary accent-4">
                  <v-card-text class="white--text mt-11">
                    <h1 class="text-center display-1">Welcome !</h1>
                    <h5 class="text-center">Enter your personal informations to start your project.</h5>
                  </v-card-text>
                  <div class="text-center">
                    <v-btn outlined dark @click="step++">SIGN UP</v-btn>
                  </div>
                </v-col>
              </v-row>
            </v-window-item>
            <v-window-item :value="2">
              <v-row class="fill-height">
                <v-col cols="12" md="4" class="primary accent-4">
                  <v-card-text class="white--text mt-11">
                    <h1 class="text-center display-1">Welcome back!</h1>
                    <h5 class="text-center">To keep connected login with your personal info.</h5>
                  </v-card-text>
                  <div class="text-center">
                    <v-btn outlined dark @click="step--">SIGN IN</v-btn>
                  </div>
                </v-col>
                <v-col cols="12" md="8">
                  <v-card-text class="mt-11">
                    <h1
                      class="text-center font-weight-bold display-2 primary--text text--accent-4"
                    >Create Account</h1>
                    <v-divider></v-divider>
                    <v-form>
                      <v-text-field
                        label="First Name"
                        name="First Name"
                        v-model="userDataRegister.first_name"
                        prepend-icon="mdi-account"
                        type="text"
                        color="primary accent-4"
                      />
                      <v-text-field
                        label="Last Name"
                        name="Last Name"
                        v-model="userDataRegister.last_name"
                        prepend-icon="mdi-account"
                        type="text"
                        color="primary accent-4"
                      />
                      <v-text-field
                        label="Email"
                        name="Email"
                        v-model="userDataRegister.email"
                        prepend-icon="mdi-email"
                        type="text"
                        color="primary accent-4"
                      />
                      <v-text-field
                        id="password"
                        label="Password"
                        name="Password"
                        v-model="userDataRegister.password"
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append="show1 = !show1"
                        :type="show1 ? 'text' : 'password'"
                        prepend-icon="mdi-lock"
                        color="primary accent-4"
                      />
                    </v-form>
                  </v-card-text>
                  <div class="text-center mt-3 mb-3">
                    <v-btn @click.prevent="signup" color="primary accent-4" dark>SIGN UP</v-btn>
                  </div>
                </v-col>
              </v-row>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    step: 1,
    userDataLogin: {
      email: "",
      password: ""
    },
    show1: false,
    userDataRegister: {
      email: "",
      first_name: "",
      last_name: "",
      password: ""
    }
  }),
  methods: {
    login() {
      this.$store
        .dispatch("userLogin", {
          email: this.userDataLogin.email,
          password: this.userDataLogin.password
        })
        .then(() => {
          console.log("test");
          this.$router.push({ name: "home" });
        })
        .catch(err => {
          console.log(err);
        });
    },
    signup() {
      this.$store
        .dispatch("userRegister", {
          email: this.userDataRegister.email,
          password: this.userDataRegister.password,
          first_name: this.userDataRegister.first_name,
          last_name: this.userDataRegister.last_name
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