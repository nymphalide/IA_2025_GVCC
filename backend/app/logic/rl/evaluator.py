from app.schemas.rl_schemas import RLAnswerRequest, RLEvaluationResponse
import math


def evaluate_rl(user_value: float, correct_value: float) -> RLEvaluationResponse:
    TOLERANCE = 0.01

    diff = abs(user_value - correct_value)

    if diff <= TOLERANCE:
        return RLEvaluationResponse(
            percentage=100,
            correct_value=round(correct_value, 4),
            explanation="Corect! Calculul se încadrează în marja de eroare acceptată."
        )
    else:
        return RLEvaluationResponse(
            percentage=0,
            correct_value=round(correct_value, 4),
            explanation=(
                f"Greșit. Valoarea calculată de tine ({user_value}) diferă de cea corectă ({round(correct_value, 4)}). "
                "Verifică formula și ordinea operațiilor."
            )
        )