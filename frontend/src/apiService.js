import axios from 'axios';

// Creăm o instanță Axios configurată
// API-ul rulează pe localhost:8000 (expus de Docker Compose)
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000, // Timp de așteptare de 5 secunde
});

/**
 * Cere o nouă problemă MinMax de la API.
 */
export const generateMinMaxProblem = () => {
  return api.post('/generate/minmax');
};

/**
 * Trimite un răspuns MinMax la API pentru evaluare.
 * @param {object} answerData - Obiectul care conține răspunsul
 * @param {number} answerData.problem_seed - Seed-ul problemei rezolvate
 * @param {number} answerData.root_value - Valoarea rădăcinii calculată de utilizator
 * @param {number} answerData.visited_nodes - Nodurile vizitate calculate de utilizator
 */
export const evaluateMinMaxAnswer = (answerData) => {
  return api.post('/evaluate/minmax', answerData);
};