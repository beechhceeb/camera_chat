import logging
from config.settings import MODEL

log = logging.getLogger(__name__)


def slugify_model_name(name):
    # Replace spaces, slashes, and dots with dashes, remove trailing dashes or dots
    dash = name.replace(' ', '-').replace('/', '-').replace('.', '-').lower().rstrip('-').rstrip('.')
    return dash


def build_chatbot_output(cameras, reason, text):
    cameras_dash = [slugify_model_name(c) for c in cameras]
    output = []
    output.append("Recommended Cameras:")
    for camera, dash in zip(cameras, cameras_dash):
        output.append(f"- [{camera}](https://www.mpb.com/en-uk/product/{dash})")
    output.append("\nReasoning:")
    output.append(reason)
    output.append("\nFurther Reading:")
    for camera in cameras:
        output.append(f"- {camera}")
        output.append(f"  - [DPReview](https://www.dpreview.com/search?query={camera.replace(' ', '%20')})")
        output.append(f"  - [PhotographyBlog](https://www.photographyblog.com/search/results?q={camera.replace(' ', '+')})")
        output.append(f"  - [Youtube](https://www.youtube.com/results?search_query={camera.replace(' ', '+')}+review)")
        output.append(f"  - [Reddit](https://www.reddit.com/search/?q={camera.replace(' ', '+')}+review)")
        # output.append(f"  - [Brand Website](https://www.google.co.uk/search?q={camera.replace(' ', '%20')}) (would be precalculated)")
    return "\n".join(output)


def get_camera_recommendation(
    client, user_description, inventory_context, previous_chat, valid_models=None
):
    prompt = f"""

    You are an extremely knowledgeable camera and lens expert who works for MPB, a used camera and lens website.
    You are here to help the user find the best three cameras or lenses for their needs.

    Based on the following camera or lens requirements:

    {user_description}

    And considering the available inventory (prices refer to excellent condition):
    
    {inventory_context}

    And previous chat history:
    
    {previous_chat}

    Please provide your recommendation in the exact following format:
    Models: <model1>, <model2>, <model3>
    Explanation: <detailed explanation encouraging the user to buy these cameras or lenses>

    Ensure the response strictly follows this format.

    """
    log.info("[PROMPT] User: %s", user_description)
    log.info("[PROMPT] Previous chat: %s", previous_chat)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )
        log.info("[PROMPT] Gemini: %s", response.text)
        models_part, explanation_part = response.text.split("Explanation:", 1)
        models_line = models_part.replace("Models:", "").strip()
        recommended_models = [
            model.strip() for model in models_line.split(",") if model.strip()
        ]
        # Check if recommended models are in inventory
        if valid_models is not None:
            missing = [m for m in recommended_models if m not in valid_models]
            if missing:
                error_msg = (
                    f"Sorry, these models are not in stock: {', '.join(missing)}"
                )
                return [], error_msg, previous_chat, prompt, error_msg
        explanation = explanation_part.strip()
        new_history = f"User: {user_description}\nGemini: {response.text}\n"
        full_history = previous_chat + new_history
        chatbot_output = build_chatbot_output(recommended_models, explanation, full_history)
        return recommended_models, explanation, full_history, prompt, chatbot_output
    except Exception:
        error_msg = (
            "Sorry, I couldn't understand your request or generate a recommendation. "
            "Please try rephrasing your question or providing more details."
        )
        return [], error_msg, previous_chat, prompt, error_msg

def build_comparison_output(cameras, explanation):
    cameras_dash = [slugify_model_name(c) for c in cameras]
    output = []
    output.append("Camera Comparison:")
    for camera, dash in zip(cameras, cameras_dash):
        output.append(f"- [{camera}](https://www.mpb.com/en-uk/product/{dash})")
    output.append("\nComparison Details:")
    output.append(explanation)
    output.append("\nFurther Reading:")
    for camera in cameras:
        output.append(f"- {camera}")
        output.append(f"  - [DPReview](https://www.dpreview.com/search?query={camera.replace(' ', '%20')})")
        output.append(f"  - [PhotographyBlog](https://www.photographyblog.com/search/results?q={camera.replace(' ', '+')})")
        output.append(f"  - [Youtube](https://www.youtube.com/results?search_query={camera.replace(' ', '+')}+review)")
        output.append(f"  - [Reddit](https://www.reddit.com/search/?q={camera.replace(' ', '+')}+review)")
        # output.append(f"  - [Brand Website](https://www.google.co.uk/search?q={camera.replace(' ', '%20')}) (would be precalculated)")
    return "\n".join(output)

def get_camera_comparison(
    client, user_description, inventory_context, previous_chat
):
    prompt = f"""

    You are an extremely knowledgeable camera and lens expert who works for MPB, a used camera and lens website.
    You are here to help the user compare two cameras or lenses for their needs.

    Based on the following camera or lens requirements or models to compare:

    {user_description}

    And considering the available inventory (prices refer to excellent condition):
    
    {inventory_context}

    And previous chat history:
    
    {previous_chat}

    Please provide your comparison in the exact following format:
    Models: <model1>, <model2>
    Comparison: <detailed comparison of the cameras or lenses, including pros and cons, and which is best for different use cases>

    Ensure the response strictly follows this format.

    """
    log.info("[PROMPT] User: %s", user_description)
    log.info("[PROMPT] Previous chat: %s", previous_chat)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )
        log.info("[PROMPT] Gemini: %s", response.text)
        models_part, explanation_part = response.text.split("Comparison:", 1)
        models_line = models_part.replace("Models:", "").strip()
        compared_models = [
            model.strip() for model in models_line.split(",") if model.strip()
        ]
        explanation = explanation_part.strip()
        new_history = f"User: {user_description}\nGemini: {response.text}\n"
        full_history = previous_chat + new_history
        chatbot_output = build_comparison_output(compared_models, explanation)
        return compared_models, explanation, full_history, prompt, chatbot_output
    except Exception:
        error_msg = (
            "Sorry, I couldn't understand your request or generate a comparison. "
            "Please try rephrasing your question or providing more details."
        )
        return [], error_msg, previous_chat, prompt, error_msg
