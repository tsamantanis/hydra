import axios from 'axios';

const api = axios.create({
    baseURL: "http://localhost:5000/",
    headers: {
        'content-type': 'application/json',
        '$binary': '',
    },
});

export default api;
