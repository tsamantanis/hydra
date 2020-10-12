import axios from 'axios';

const api = axios.create({
    baseURL: "http://localhost:5000/",
    headers: {
        'content-type': 'application/json'
    },
});

// api.defaults.headers.common['Authorization'] = 'Bearer ' + token;

export default api;
