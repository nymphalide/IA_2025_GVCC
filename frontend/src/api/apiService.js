import axios from 'axios';

// Create configured Axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000, 
});

// --- MINMAX ENDPOINTS ---
// Actualizat pentru a accepta parametri de configurare
export const generateMinMaxProblem = (config = {}) => {
  return api.post('/generate/minmax', config);
};

export const evaluateMinMaxAnswer = (answerData) => {
  return api.post('/evaluate/minmax', answerData);
};

// --- NASH ENDPOINTS ---
export const generateNashProblem = (config = {}) => {
    // config example: { rows: 3, cols: 3, random_size: false }
    return api.post('/generate/nash', config);
};

export const evaluateNashAnswer = (answerData) => {
    return api.post('/evaluate/nash', answerData);
};

// --- STRATEGY ENDPOINTS ---
export const generateStrategyProblem = () => {
  return api.post('/generate/strategy');
};

export const evaluateStrategyAnswer = (answerData) => {
  return api.post('/evaluate/strategy', answerData);
};

export default api;