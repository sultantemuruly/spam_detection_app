import axios from 'axios'

const api = axios.create({
    baseURL: 'https://tranquil-emotion-production.up.railway.app',
})

export default api;
