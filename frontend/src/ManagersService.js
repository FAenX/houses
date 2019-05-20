import axios from 'axios';
const API_URL = 'http://localhost:8000';

export default class ManagerService{

    constructor(){}


    getManagers() {
        const url = `${API_URL}/api/managers/`;
        return axios.get(url).then(response => response.data);
    }  
    getManagersByURL(link){
        const url = `${API_URL}${link}`;
        return axios.get(url).then(response => response.data);
    }
    getManager(pk) {
        const url = `${API_URL}/api/managers/${pk}`;
        return axios.get(url).then(response => response.data);
    }
    deleteManager(manager){
        const url = `${API_URL}/api/managers/${manager.pk}`;
        return axios.delete(url);
    }
    createManagers(manager){
        const url = `${API_URL}/api/managers/`;
        return axios.post(url,manager);
    }
    updateManagers(manager){
        const url = `${API_URL}/api/managers/${manager.pk}`;
        return axios.put(url,manager);
    }
}
