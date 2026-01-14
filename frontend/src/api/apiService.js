import axios from 'axios';

// Create configured Axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000, 
});

// ... (MinMax, Nash, Strategy existing code) ...

// --- MINMAX ENDPOINTS ---
export const generateMinMaxProblem = (config = {}) => {
  return api.post('/generate/minmax', config);
};
export const evaluateMinMaxAnswer = (answerData) => {
  return api.post('/evaluate/minmax', answerData);
};

// --- NASH ENDPOINTS ---
export const generateNashProblem = (config = {}) => {
    return api.post('/generate/nash', config);
};
export const evaluateNashAnswer = (answerData) => {
    return api.post('/evaluate/nash', answerData);
};

// --- STRATEGY ENDPOINTS ---
export const generateStrategyProblem = (config = {}) => {
  return api.post('/generate/strategy', config);
};
export const evaluateStrategyAnswer = (answerData) => {
  return api.post('/evaluate/strategy', answerData);
};

export const generateRLProblem = (config) => {
  return api.post('/generate/rl', config);
};

export const evaluateRLAnswer = (answerData) => {
  return api.post('/evaluate/rl', answerData);
// --- CSP ENDPOINTS (NEW) ---
export const generateCspProblem = (config = {}) => {
    return api.post('/generate/csp', config);
};

export const evaluateCspAnswer = (answerData) => {
    return api.post('/evaluate/csp', answerData);
};

export default api;