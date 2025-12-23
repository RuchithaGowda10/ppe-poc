from app.lms.ppe_policy import LAB_PPE_RULES

class DecisionEngine:
    def evaluate(self, lab_id: str, detected_ppe: list):
        required = LAB_PPE_RULES.get(lab_id, [])
        missing = [ppe for ppe in required if ppe not in detected_ppe]

        return {
            "compliant": len(missing) == 0,
            "detected_ppe": detected_ppe,
            "required_ppe": required,
            "missing_ppe": missing
        }
