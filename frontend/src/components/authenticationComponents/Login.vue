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
                      class="mb-4 text-center font-weight-bold display-2 teal--text text--accent-4"
                    >Sign In DataLinked !</h1>
                    <v-divider></v-divider>
                    <div class="mt-3 text-center">
                      <h3>Sign in with your google account</h3>
                      <v-spacer></v-spacer>
                      <v-btn
                        @click="authenticate('google')"
                        class="mt-2 mb-4 color white--text teal accent-4"
                      >
                        <v-icon class="mr-2">mdi-gmail</v-icon>Sign in with Google
                      </v-btn>
                    </div>
                    <v-divider></v-divider>
                    <h4 class="text-center mt-3">Or enter your email</h4>
                    <v-form>
                      <v-text-field
                        label="Email"
                        name="Email"
                        prepend-icon="mdi-email"
                        type="text"
                        color="teal accent-4"
                      />
                      <v-text-field
                        id="password"
                        label="Password"
                        name="Password"
                        prepend-icon="mdi-lock"
                        type="password"
                        color="teal accent-4"
                      />
                    </v-form>
                    <h3 class="text-right mt-3">Forget your password ?</h3>
                  </v-card-text>
                  <div class="text-center mt-3 mb-3">
                    <v-btn color="teal accent-4" dark>SIGN IN</v-btn>
                  </div>
                </v-col>
                <v-col cols="12" md="4" class="teal accent-4">
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
                <v-col cols="12" md="4" class="teal accent-4">
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
                      class="text-center font-weight-bold display-2 teal--text text--accent-4"
                    >Create Account</h1>
                    <v-divider></v-divider>

                    <v-form>
                      <v-text-field
                        label="Name"
                        name="Name"
                        prepend-icon="mdi-person"
                        type="text"
                        color="teal accent-4"
                      />
                      <v-text-field
                        label="Email"
                        name="Email"
                        prepend-icon="mdi-email"
                        type="text"
                        color="teal accent-4"
                      />
                      <v-text-field
                        id="password"
                        label="Password"
                        name="Password"
                        prepend-icon="mdi-lock"
                        type="password"
                        color="teal accent-4"
                      />
                    </v-form>
                  </v-card-text>
                  <div class="text-center mt-3 mb-3">
                    <v-btn color="teal accent-4" dark>SIGN IN</v-btn>
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
import { authMixin } from '../../mixins/authMixin'

export default {
    mixins: [ authMixin ],
  data: () => ({
    step: 1
  }),
  props: {
    source: String
  }
};
</script>