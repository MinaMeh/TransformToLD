<template>
  <div style="padding: 2rem 3rem; text-align: left;">
    <div class="field">
      <label class="label">Project Name</label>
      <div class="control">
        <input
          :class="['input', ($v.form.project_name.$error) ? 'is-danger' : '']"
          type="text"
          placeholder="Project Name"
          v-model="form.project_name"
        />
      </div>
      <p v-if="$v.form.project_name.$error" class="help is-danger">This project name is invalid</p>
    </div>
    <div class="field">
      <label class="label">File Link</label>
      <div class="control">
        <input
          :class="['input', ($v.form.file_link.$error) ? 'is-danger' : '']"
          type="text"
          placeholder="File Link"
          v-model="form.file_link"
        />
      </div>
      <p v-if="$v.form.file_link.$error" class="help is-danger">This file link is invalid</p>
    </div>
    <div class="field">
      <label class="label">Vocabularies</label>
      <div class="control">
        <div class="tags">
          <span class="tag is-link">
            foaf
            <button class="delete is-small"></button>
          </span>
          <span class="tag is-link">
            vcard
            <button class="delete is-small"></button>
          </span>
          <span class="tag is-link">
            rdfs
            <button class="delete is-small"></button>
          </span>
        </div>
      </div>
    </div>
    <table class="table is-bordered">
      <thead>
        <tr>
          <th>Prefix</th>
          <th>URI</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>foaf</td>
          <td>
            <a href="http://xmlns.com">http://xmlns.com</a>
          </td>
          <td>
            <button class="button is-success">add</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
export default {
  props: ["clickedNext", "currentStep"],
  mixins: [validationMixin],
  data() {
    return {
      form: {
        project_name: "",
        file_link: ""
      }
    };
  },
  validations: {
    form: {
      project_name: {
        required
      },
      file_link: {
        required
      }
    }
  },
  watch: {
    $v: {
      handler: function(val) {
        if (!val.$invalid) {
          this.$emit("can-continue", { value: true });
        } else {
          this.$emit("can-continue", { value: false });
        }
      },
      deep: true
    },
    clickedNext(val) {
      if (val === true) {
        this.$v.form.$touch();
      }
    }
  },
  mounted() {
    if (!this.$v.$invalid) {
      this.$emit("can-continue", { value: true });
    } else {
      this.$emit("can-continue", { value: false });
    }
  }
};
</script>
