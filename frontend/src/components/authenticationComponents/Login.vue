<template>
  <div>
    <section class="hero is-primary is-fullheight">
      <!-- Hero content: will be in the middle -->
      <div class="hero-body">
        <div class="container has-text-center">
          <h1 class="subtitle">
            <g-signin-button
              :params="googleSignInParams"
              @success="onSignInSuccess"
              @error="onSignInError"
            >
              Sign in with Google
            </g-signin-button>
          </h1>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
//import GSignInButton from 'vue-google-signin-button'

export default {
  components: {
    // GSignInButton,
  },
  data() {
    return {
      googleSignInParams: {
        client_id:
          "265982645018-0qvdbb07ltu6uou8j4pbdelk76l1evef.apps.googleusercontent.com",
        scope: "profile email",
      },
    };
  },
  methods: {
    onSignInSuccess(googleUser) {
      var profile = googleUser.getBasicProfile();
      this.$store
        .dispatch("login", {
          access_token: googleUser.getAuthResponse().access_token,
        })
        .then(() => {
          console.log("login successful!!");
          console.log("ID: " + profile.getId()); // Don't send this directly to your server!
          console.log("Full Name: " + profile.getName());
          console.log("Given Name: " + profile.getGivenName());
          console.log("Family Name: " + profile.getFamilyName());
          console.log("Image URL: " + profile.getImageUrl());
          console.log("Email: " + profile.getEmail());
        });
    },
    onSignInError(error) {
      console.log("OH NOES", error);
    },
  },
};
</script>

<style>
.g-signin-button {
  /* This is where you control how the button looks. Be creative! */
  display: inline-block;
  padding: 4px 8px;
  border-radius: 3px;
  background-color: #3c82f7;
  color: #fff;
  box-shadow: 0 3px 0 #0f69ff;
}
</style>
