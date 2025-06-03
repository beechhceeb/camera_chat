from flask import Flask, render_template, request, jsonify
import logging
from services import search_service

app = Flask(__name__)
log = logging.getLogger(__name__)

