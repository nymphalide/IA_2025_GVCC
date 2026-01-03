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
export const generateStrategyProblem = () => {
  return api.post('/generate/strategy');
};
export const evaluateStrategyAnswer = (answerData) => {
  return api.post('/evaluate/strategy', answerData);
};

// --- CSP ENDPOINTS (NEW) ---
export const generateCspProblem = (config = {}) => {
    return api.post('/generate/csp', config);
};

export const evaluateCspAnswer = (answerData) => {
    return api.post('/evaluate/csp', answerData);
};

// --- BAYES ENDPOINTS ---
export const generateBayesProblem = (config = {}) => {
  return api.get('/bayes/generate', { params: config });
};

export const evaluateBayesAnswer = (answerData) => {
  return api.post('/bayes/evaluate', answerData);
};

export default api;