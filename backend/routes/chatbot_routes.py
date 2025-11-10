import time
from flask import Blueprint, request, jsonify, current_app
from services.chatbot_service import build_prompt, call_gemini, ground_answer

chatbot_bp = Blueprint('chatbot_bp', __name__)

MAX_QUESTION = 500
FALLBACK = "No idea based on brochure."


def _summary(text: str, n: int = 200) -> str:
    t = (text or '').replace('\n', ' ')
    return t[:n]


@chatbot_bp.route('/chatbot/query', methods=['POST'])
def chatbot_query():
    ts = time.time()
    data = request.get_json(silent=True) or {}
    question = (data.get('question') or '').strip()
    context = data.get('context') or {}

    if not question:
        return jsonify({'status': 'error', 'message': 'question required'}), 400
    if len(question) > MAX_QUESTION:
        question = question[:MAX_QUESTION]

    prompt = build_prompt(question, context)
    raw_txt, meta = call_gemini(prompt)
    obj = ground_answer(question, context, raw_txt)

    dur = round((time.time() - ts) * 1000)
    try:
        current_app.logger.info('chatbot.query', extra={'context': {
            'duration_ms': dur,
            'q_len': len(question),
            'ctx_keys': list(context.keys()) if isinstance(context, dict) else [],
            'answer_summary': _summary(obj.get('answer', '')),
            'fallback': obj.get('answer') == FALLBACK,
        }})
    except Exception:
        pass

    return jsonify({'answer': obj.get('answer', FALLBACK)}), 200
