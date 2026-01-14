import axios from 'axios';

// Create configured Axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000, 
});

// --- MINMAX ENDPOINTS ---
export const generateMinMaxProblem = () => {
  return api.post('/generate/minmax');
};

export const evaluateMinMaxAnswer = (answerData) => {
  return api.post('/evaluate/minmax', answerData);
};

// --- NASH ENDPOINTS (MODIFIED) ---
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

export const generateRLProblem = (config) => {
  return api.post('/generate/rl', config);
};

export const evaluateRLAnswer = (answerData) => {
  return api.post('/evaluate/rl', answerData);
};

export default api;