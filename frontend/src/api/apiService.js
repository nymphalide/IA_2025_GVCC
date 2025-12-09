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

// --- NASH EQUILIBRIUM ENDPOINTS (Placeholder) ---
// You will implement these in the next step
export const generateNashProblem = () => {
    // return api.post('/generate/nash');
    return Promise.resolve({ data: {} }); // Temp mock
};

export const evaluateNashAnswer = (answerData) => {
    // return api.post('/evaluate/nash', answerData);
    return Promise.resolve({ data: {} }); // Temp mock
};