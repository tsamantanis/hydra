import axios from 'axios';

const api = axios.create({
    baseURL: "http://localhost:5000",
    method:'post',
    // url:"http://localhost:5000/send",
    headers: {'content-type': 'application/json'},
    // data: this.state
});

export default api;
