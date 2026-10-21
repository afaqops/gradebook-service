
from errors import ValidationError

MAX_TOTAL_WEIGHT = 100
TOLERANCE = 1e-9


def ensure_weight_fits(existing_weights, new_weight):
    if sum(existing_weights) + new_weight > MAX_TOTAL_WEIGHT + TOLERANCE:
        raise ValidationError("Assessment weights cannot exceed 100.")

