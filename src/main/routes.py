from flask import Blueprint, request, jsonify, render_template
from services.chat import get_camera_recommendation
from core.prompt import get_camera_comparison
from config.settings import QUERY, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_DATASET, GOOGLE_CLOUD_LOCATION, GOOGLE_GENAI_USE_VERTEXAI
from core.dataset import format_inventory_context
from services.dataset import get_data
from services.bq_helper import BQHelper
from google import genai
from google.genai.types import HttpOptions

bp = Blueprint('main', __name__)

# Initialize BQ and inventory context once (for demo; in production, cache or reload as needed)
bq = BQHelper(
    billing_project_id=GOOGLE_CLOUD_PROJECT,
    write_project_id=GOOGLE_CLOUD_PROJECT,
    read_project_id=GOOGLE_CLOUD_PROJECT,
    write_dataset=GOOGLE_CLOUD_DATASET,
    read_dataset=GOOGLE_CLOUD_DATASET,
    daw_dataset=GOOGLE_CLOUD_DATASET,
    sql_folder="sql",
)
df = get_data(bq, query=QUERY)
inventory_context = format_inventory_context(df)

client = genai.Client(
    http_options=HttpOptions(api_version="v1"),
    vertexai=GOOGLE_GENAI_USE_VERTEXAI,
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    previous_chat = data.get("history", "")
    mode = data.get("mode", "recommend")
    valid_models = set(df["model_name"].unique())
    if mode == "compare":
        cameras, reason, history, prompt, chatbot_output = get_camera_comparison(
            client, user_message, inventory_context, previous_chat, valid_models=valid_models
        )
    else:
        cameras, reason, history, prompt, chatbot_output = get_camera_recommendation(
            client, user_message, inventory_context, previous_chat, valid_models=valid_models
        )
    return jsonify({
        "cameras": cameras,
        "reason": reason,
        "chatbot_output": chatbot_output,
        "history": history
    })
