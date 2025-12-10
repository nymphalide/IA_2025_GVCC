import axios from 'axios';

// Create configured Axios instance
// API runs on localhost:8000 (exposed by Docker Compose)
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000, 
});

// --- MINMAX ENDPOINTS (L6) ---

/**
 * Request a new MinMax problem.
 */
export const generateMinMaxProblem = () => {
  return api.post('/generate/minmax');
};

/**
 * Send MinMax answer for evaluation.
 */
export const evaluateMinMaxAnswer = (answerData) => {
  return api.post('/evaluate/minmax', answerData);
};

export const generateNashProblem = () => {
    return api.post('/generate/nash'); // Ensure this matches backend @router.post("/generate/nash")
};

export const evaluateNashAnswer = (answerData) => {
    return api.post('/evaluate/nash', answerData);
};


export const generateStrategyProblem = () => {
  return api.post('/generate/strategy');
};

export const evaluateStrategyAnswer = (answerData) => {
  return api.post('/evaluate/strategy', answerData);
};

export default api;