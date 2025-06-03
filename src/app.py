from flask import Flask
from services.chat import get_camera_recommendation, output_message
from config.logger import logging
from config.settings import (
    GOOGLE_GENAI_USE_VERTEXAI,
    GOOGLE_CLOUD_PROJECT,
    GOOGLE_CLOUD_LOCATION,
    GOOGLE_CLOUD_DATASET,
    QUERY,
)
from core.prompt import format_inventory_context
from services.dataset import get_data
from services.bq_helper import BQHelper
from google import genai
from google.genai.types import HttpOptions

app = Flask(__name__)
log = logging.getLogger(__name__)
bq = BQHelper(
    billing_project_id=GOOGLE_CLOUD_PROJECT,
    write_project_id=GOOGLE_CLOUD_PROJECT,
    read_project_id=GOOGLE_CLOUD_PROJECT,
    write_dataset=GOOGLE_CLOUD_DATASET,
    read_dataset=GOOGLE_CLOUD_DATASET,
    daw_dataset=GOOGLE_CLOUD_DATASET,
    sql_folder="",
)

df = get_data(bq, query=QUERY)

user_description = "I want a vintage looking small lightweight interchangeable lens camera with a good battery life and 4k video recording. I am looking for something that is not too expensive, ideally under £500."


inventory_context = format_inventory_context(df)

client = genai.Client(
    http_options=HttpOptions(api_version="v1"),
    vertexai=GOOGLE_GENAI_USE_VERTEXAI,
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)

cameras, reason, text, prompt = get_camera_recommendation(
    client, user_description, inventory_context, previous_chat=""
)
output_message(cameras, reason, text)


cameras, reason, text, prompt = get_camera_recommendation(client, "Surely there is something cheaper", inventory_context, previous_chat=text)
output_message(cameras, reason, text)


cameras, reason, text, prompt = get_camera_recommendation(client, "CHeaper!!!", inventory_context, previous_chat=text)
output_message(cameras, reason, text)