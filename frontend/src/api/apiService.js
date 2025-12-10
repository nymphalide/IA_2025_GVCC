import axios from 'axios';

// Create configured Axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000,
});

// --- MINMAX ENDPOINTS (L6) ---

export const generateMinMaxProblem = () => {
  return api.post('/generate/minmax');
};

export const evaluateMinMaxAnswer = (answerData) => {
  return api.post('/evaluate/minmax', answerData);
};

// --- NASH EQUILIBRIUM ENDPOINTS (Placeholder) ---

export const generateNashProblem = () => {
  return Promise.resolve({ data: {} });
};

export const evaluateNashAnswer = (answerData) => {
  return Promise.resolve({ data: {} });
};

// --- NQUEENS ENDPOINTS (ACTUAL NEW ONES) ---

export const generateStrategyProblem = () => {
  return api.post('/generate/strategy');
};

export const evaluateStrategyAnswer = (answerData) => {
  return api.post('/evaluate/strategy', answerData);
};

export default api;
