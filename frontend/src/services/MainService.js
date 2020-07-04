import axios from "axios";
var instance = axios.create({
  baseURL: "http://localhost:8000/",
});

export default instance;
