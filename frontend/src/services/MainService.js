import axios from "axios";
var instance = axios.create({
  baseURL: "http://localhost:8000/",
  headers: { Authorization: `JWT ${localStorage.getItem("t")}` },
});

export default instance;
