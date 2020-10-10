import axios from 'axios';

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    method:'post',
    // url:"http://localhost:5000/send",
    headers: {'content-type': 'application/json'},
    // data: this.state
});

export default api;
