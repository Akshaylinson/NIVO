"""Explicit simulation signatures, kept separate from any trainable model."""
from backend.app.core.schemas import Intent

# These are development labels for reproducible public/mock artifacts, not a
# claim that a frequency band can decode a person's thoughts.
PUBLIC_SIGNATURE_ROUTING = {
    "RESTING_BASELINE": {"wake": False, "intent": None, "description": "NO WAKE"},
    "ALPHA_WAKE_CUE": {"wake": True, "intent": None, "description": "NIVO wake cue"},
    "MOTOR_IMAGERY_LEFT": {"wake": True, "intent": Intent.NEXT, "description": "NEXT"},
    "MOTOR_IMAGERY_RIGHT": {"wake": True, "intent": Intent.SELECT, "description": "SELECT"},
    "SEARCH_SIGNATURE": {"wake": True, "intent": Intent.SEARCH, "description": "SEARCH"},
}
