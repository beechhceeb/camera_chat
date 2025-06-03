from config.settings import MODEL


def get_camera_recommendation(
    client, user_description, inventory_context, previous_chat
):
    prompt = f"""

    You are an extremely knowledgeable camera expert who works for MPB, a used camera website.
    You are here to help the user find the best three cameras for their needs.

    Based on the following camera requirements:

    {user_description}

    And considering the available inventory (prices refer to max):
    {inventory_context}

    And previous chat history:
    {previous_chat}

    Please provide your recommendation in the exact following format:
    Models: <model1>, <model2>, <model3>
    Explanation: <detailed explanation encouraging the user to buy these cameras>

    Ensure the response strictly follows this format.

    """
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    models_part, explanation_part = response.text.split("Explanation:", 1)
    models_line = models_part.replace("Models:", "").strip()
    recommended_models = [
        model.strip() for model in models_line.split(",") if model.strip()
    ]
    explanation = explanation_part.strip()

    return recommended_models, explanation, previous_chat + response.text, prompt
