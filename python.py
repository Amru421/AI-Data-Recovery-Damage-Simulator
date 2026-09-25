import os
import streamlit as st
import json
import random
import re
from openai import OpenAI

# ==========================================
# 1. PAGE CONFIGURATION & INITIAL DATA
# ==========================================
st.set_page_config(page_title="AI Data Recovery Lab", layout="wide")

GROUND_TRUTH = [
    {
        "transaction_id": "TXN-9901",
        "timestamp": "2026-09-25T14:32:00Z",
        "user_id": 1042,
        "amount_usd": 249.50,
        "action": "PURCHASE",
        "status": "SUCCESS"
    },
    {
        "transaction_id": "TXN-9902",
        "timestamp": "2026-09-25T14:33:15Z",
        "user_id": 8821,
        "amount_usd": 12.00,
        "action": "SUBSCRIPTION_RENEW",
        "status": "SUCCESS"
    },
    {
        "transaction_id": "TXN-9903",
        "timestamp": "2026-09-25T14:35:00Z",
        "user_id": 3310,
        "amount_usd": 0.00,
        "action": "LOGIN_ATTEMPT",
        "status": "FAILED"
    }
]

# ==========================================
# 2. DAMAGE SIMULATOR ENGINE ("THE SCISSORS")
# ==========================================
def corrupt_dataset(data, damage_type, intensity):
    """Corrupts data based on selected damage type and intensity (10% to 90%)."""
    raw_str = json.dumps(data, indent=2)
    
    if damage_type == "Truncation (Chop End)":
        cut_len = int(len(raw_str) * (1 - (intensity / 100)))
        return raw_str[:cut_len]

    corrupted_data = json.loads(json.dumps(data))  # Deep copy
    
    for record in corrupted_data:
        keys = list(record.keys())
        num_keys_to_affect = max(1, int(len(keys) * (intensity / 100)))
        chosen_keys = random.sample(keys, num_keys_to_affect)

        for key in chosen_keys:
            if damage_type == "Field Obliteration (Delete)":
                del record[key]
            elif damage_type == "Type Mangling (Noise)":
                record[key] = "###CORRUPTED_NOISE###"
                
    return json.dumps(corrupted_data, indent=2)

# ==========================================
# 3. AI RECOVERY ENGINE
# ==========================================
def quick_heuristic_fix(broken_str):
    """Stage 1: Basic structural syntax repair."""
    fixed = broken_str.strip()
    # Auto-close brackets if truncated
    open_curly = fixed.count('{') - fixed.count('}')
    open_square = fixed.count('[') - fixed.count(']')
    
    if fixed.endswith(','):
        fixed = fixed[:-1]
    
    fixed += '}' * max(0, open_curly)
    fixed += ']' * max(0, open_square)
    return fixed

def run_ai_recovery(damaged_str, api_key):
    """Stage 2: LLM Context Completion."""
    # Step 1: Apply syntax heuristic pass
    staged_str = quick_heuristic_fix(damaged_str)
    
    # Prefer an environment variable if the user has not pasted a key manually.
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()

    # If no API key is provided, run offline demo recovery fallback
    if not api_key:
        st.warning("⚠️ No OpenAI API key provided. Running offline mock recovery.")
        return json.dumps(GROUND_TRUTH, indent=2)
    
    # Call OpenAI API
    try:
        client = OpenAI(api_key=api_key)
        prompt = f"""
        You are an expert Data Forensic AI. 
        Below is a damaged/truncated JSON dataset representing system transaction logs.
        
        Expected Schema per record:
        - transaction_id (string: 'TXN-XXXX')
        - timestamp (ISO String)
        - user_id (integer)
        - amount_usd (float)
        - action (string: 'PURCHASE', 'LOGIN_ATTEMPT', etc.)
        - status (string: 'SUCCESS', 'FAILED')

        DAMAGED DATA:
        {staged_str}

        TASK: Reconstruct the missing or corrupted JSON values logically based on context and format. 
        Return ONLY valid JSON array with no markdown explanations.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = response.choices[0].message.content.strip()
        # Clean potential markdown formatting
        clean_json = re.sub(r'^```json\s*|\s*```$', '', content, flags=re.MULTILINE)
        return clean_json
    except Exception as e:
        return f"Error running AI recovery: {str(e)}"

# ==========================================
# 4. EVALUATION METRICS
# ==========================================
def calculate_accuracy(recovered_str, ground_truth):
    """Calculate accuracy score against ground truth."""
    try:
        recovered_json = json.loads(recovered_str)
        if not isinstance(recovered_json, list) or len(recovered_json) == 0:
            return False, 0.0
        
        total_fields = 0
        correct_fields = 0
        
        for idx, gt_record in enumerate(ground_truth):
            if idx >= len(recovered_json):
                break
            rec_record = recovered_json[idx]
            for key, val in gt_record.items():
                total_fields += 1
                if key in rec_record and str(rec_record[key]) == str(val):
                    correct_fields += 1
                    
        score = (correct_fields / total_fields) * 100 if total_fields > 0 else 0
        return True, round(score, 1)
    except:
        return False, 0.0


def calculate_recovery_metrics(recovered_data, ground_truth):
    """Compute integrity and recovery metrics from recovered data and ground truth."""
    if not recovered_data:
        return {
            "valid": False,
            "accuracy": 0.0,
            "integrity_score": 0.0,
            "recovery_confidence": 0.0,
            "missing_records": len(ground_truth),
            "corruption_ratio": 100.0,
        }

    try:
        recovered_json = recovered_data if isinstance(recovered_data, list) else json.loads(recovered_data)
        if not isinstance(recovered_json, list):
            raise ValueError("Recovered data must be a list")
    except Exception:
        return {
            "valid": False,
            "accuracy": 0.0,
            "integrity_score": 0.0,
            "recovery_confidence": 0.0,
            "missing_records": len(ground_truth),
            "corruption_ratio": 100.0,
        }

    total_fields = 0
    correct_fields = 0
    missing_records = 0

    for idx, gt_record in enumerate(ground_truth):
        if idx >= len(recovered_json):
            missing_records += 1
            continue

        rec_record = recovered_json[idx]
        if not isinstance(rec_record, dict):
            missing_records += 1
            continue

        for key, val in gt_record.items():
            total_fields += 1
            if key in rec_record and str(rec_record[key]) == str(val):
                correct_fields += 1

    accuracy = (correct_fields / total_fields) * 100 if total_fields else 0.0
    recovered_count = min(len(recovered_json), len(ground_truth))
    missing_records += max(0, len(ground_truth) - recovered_count)
    integrity_score = max(0.0, min(100.0, accuracy))
    recovery_confidence = min(100.0, max(0.0, accuracy + 8))
    corruption_ratio = max(0.0, 100.0 - integrity_score)

    return {
        "valid": True,
        "accuracy": round(accuracy, 1),
        "integrity_score": round(integrity_score, 1),
        "recovery_confidence": round(recovery_confidence, 1),
        "missing_records": missing_records,
        "corruption_ratio": round(corruption_ratio, 1),
    }


def prioritize_recovery(metrics):
    """Assign a recovery priority level using explainable conditions."""
    accuracy = metrics.get("accuracy", 0)
    integrity_score = metrics.get("integrity_score", 0)
    confidence = metrics.get("recovery_confidence", 0)
    missing_records = metrics.get("missing_records", 0)
    corruption_ratio = metrics.get("corruption_ratio", 0)

    if accuracy >= 90 and integrity_score >= 80 and confidence >= 85 and missing_records <= 1:
        level = "HIGH"
        reason = "High-priority recovery: strong accuracy, robust integrity, and low data loss."
    elif accuracy >= 70 and integrity_score >= 60:
        level = "MEDIUM"
        reason = "Medium-priority recovery: partial reconstruction is viable with limited corruption."
    else:
        level = "LOW"
        reason = "Low-priority recovery: multiple fields are missing or heavily corrupted."

    if corruption_ratio > 50:
        reason += " Data integrity is weak and should be reviewed manually."

    return {
        "level": level,
        "reason": reason,
        "score": round((accuracy * 0.4) + (integrity_score * 0.35) + (confidence * 0.25), 1),
    }


def generate_fragment_dataset(data, damage_type, intensity):
    """Generate a synthetic fragment dataset with tracked missing and damaged records."""
    fragments = []
    for idx, record in enumerate(data, start=1):
        fragment = {
            "fragment_id": f"frag_{idx:03d}",
            "source_record": record,
            "estimated_type": "JSON_RECORD",
            "size_bytes": 128 + idx * 12,
            "confidence": max(0.4, 1.0 - (intensity / 100.0) * 0.5),
            "status": "intact",
        }
        if damage_type == "Field Obliteration (Delete)" and idx % 3 == 0:
            fragment["status"] = "missing"
        elif damage_type == "Truncation (Chop End)" and idx % 2 == 0:
            fragment["status"] = "corrupted"
        elif damage_type == "Type Mangling (Noise)" and idx % 4 == 0:
            fragment["status"] = "corrupted"
        fragments.append(fragment)

    missing_fragments = sum(1 for fragment in fragments if fragment["status"] == "missing")
    corrupted_fragments = sum(1 for fragment in fragments if fragment["status"] == "corrupted")

    return {
        "fragments": fragments,
        "missing_fragments": missing_fragments,
        "corrupted_fragments": corrupted_fragments,
        "damage_type": damage_type,
        "intensity": intensity,
        "recovery_hint": "Prioritize records that preserve schema integrity and transaction structure.",
    }


def build_forensic_report(metrics, filename):
    """Build explainable forensic-style report output for a reconstructed artifact."""
    priority = prioritize_recovery(metrics)
    return (
        f"Recovery Report for: {filename}\n"
        f"Status: {priority['level']} priority\n"
        f"Integrity: {metrics.get('integrity_score', 0)}%\n"
        f"Accuracy: {metrics.get('accuracy', 0)}%\n"
        f"Confidence: {metrics.get('recovery_confidence', 0)}%\n"
        f"Missing Records: {metrics.get('missing_records', 0)}\n"
        f"Corruption Ratio: {metrics.get('corruption_ratio', 0)}%\n"
        f"Assessment: {priority['reason']}"
    )

# ==========================================
# 5. DASHBOARD UI LAYOUT
# ==========================================
def main():
    st.title("🛡️ AI Data Recovery & Damage Simulator")
    st.caption("Live End-to-End Investigation & Restoration Pipeline")

    # Sidebar Controls
    with st.sidebar:
        st.header("⚙️ Control Panel")
        env_api_key = os.getenv("OPENAI_API_KEY", "").strip()
        api_key = st.text_input(
            "OpenAI API Key (Optional)",
            value=env_api_key,
            type="password",
            help="If left blank, the app will look for OPENAI_API_KEY in the environment."
        )
        
        st.subheader("1. Damage Configuration")
        damage_type = st.selectbox(
            "Select Corruption Method",
            ["Field Obliteration (Delete)", "Truncation (Chop End)", "Type Mangling (Noise)"]
        )
        intensity = st.slider("Damage Intensity (%)", min_value=10, max_value=80, value=40, step=10)
        
        st.divider()
        inject_btn = st.button("🔴 Inject Damage", use_container_width=True)
        recover_btn = st.button("🟢 Run AI Recovery Engine", use_container_width=True)

    # Session State Storage
    if "damaged_data" not in st.session_state:
        st.session_state.damaged_data = json.dumps(GROUND_TRUTH, indent=2)
    if "recovered_data" not in st.session_state:
        st.session_state.recovered_data = None

    # Button Handlers
    if inject_btn:
        st.session_state.damaged_data = corrupt_dataset(GROUND_TRUTH, damage_type, intensity)
        st.session_state.recovered_data = None

    if recover_btn:
        with st.spinner("AI Engine recovering data context..."):
            st.session_state.recovered_data = run_ai_recovery(
                st.session_state.damaged_data, api_key
            )

    metrics = calculate_recovery_metrics(
        st.session_state.recovered_data if st.session_state.recovered_data else None,
        GROUND_TRUTH
    )
    is_valid = metrics["valid"]
    accuracy_score = metrics["accuracy"]
    priority = prioritize_recovery(metrics)
    forensic_report = build_forensic_report(metrics, "recovered_transactions.json")

    m1, m2, m3 = st.columns(3)
    m1.metric("Ground Truth Records", len(GROUND_TRUTH))
    m2.metric("Schema Validity", "PASS ✅" if is_valid else ("PENDING ⏳" if not st.session_state.recovered_data else "FAIL ❌"))
    m3.metric("Field Accuracy Score", f"{accuracy_score}%" if st.session_state.recovered_data else "N/A")

    st.subheader("Recovery Priority")
    st.info(f"{priority['level']} — {priority['reason']}")

    st.subheader("Forensic Recovery Report")
    st.code(forensic_report, language="text")
    st.divider()

    # Main View Columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚨 Damaged Dataset (Corrupted)")
        dataset_summary = generate_fragment_dataset(GROUND_TRUTH, "Field Obliteration (Delete)", 33)
        st.json(dataset_summary)
        st.code(st.session_state.damaged_data, language="json", height=300)

    with col2:
        st.subheader("✨ AI Recovered Dataset")
        if st.session_state.recovered_data:
            st.code(st.session_state.recovered_data, language="json", height=380)
        else:
            st.info("Click 'Run AI Recovery Engine' to initiate contextual restoration.")


if __name__ == "__main__":
    main()