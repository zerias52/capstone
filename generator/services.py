# generator/services.py
import anthropic
from django.conf import settings


def generate_social_post(platform, content_topic, brand_voice, target_audience, call_to_action, key_points,
                         post_length):
    client = anthropic.Client(api_key=settings.ANTHROPIC_API_KEY)

    # Construct the prompt
    prompt = f"""Generate a social media post for {platform} with these parameters:
    Topic: {content_topic}
    Brand Voice: {brand_voice}
    Target Audience: {target_audience}
    Key Points: {key_points}
    Length: {post_length}
    """
    if call_to_action:
        prompt += f"\nCall to Action: {call_to_action}"

    # Call Claude API
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.7,
        system="You are a professional social media content creator. Create engaging, platform-appropriate content.",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return message.content