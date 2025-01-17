import anthropic
from django.conf import settings


def generate_social_post(platform, content_topic, brand_voice, target_audience,
                         call_to_action, key_points, post_length):
    """
    Generate a social media post using Claude API with consistent formatting
    """
    client = anthropic.Client(api_key=settings.ANTHROPIC_API_KEY)

    # Define platform-specific constraints
    platform_guidelines = {
        'LinkedIn': {
            'char_limit': 3000,
            'style': 'professional and insightful',
            'format': 'well-structured paragraphs with clear spacing',
            'hashtags': '3-5 relevant industry hashtags'
        },
        'Twitter': {
            'char_limit': 280,
            'style': 'concise and engaging',
            'format': 'punchy single paragraph',
            'hashtags': '1-2 trending or relevant hashtags'
        },
        'Instagram': {
            'char_limit': 2200,
            'style': 'visual and engaging',
            'format': 'easily scannable with line breaks',
            'hashtags': '5-10 relevant hashtags'
        },
        'Facebook': {
            'char_limit': 63206,
            'style': 'conversational and community-focused',
            'format': 'readable paragraphs with good spacing',
            'hashtags': '2-3 broad topic hashtags'
        }
    }

    # Enhanced system prompt with more specific guidance
    system_prompt = """You are an expert social media content creator with deep knowledge of platform-specific best practices. 
    Your task is to create engaging, platform-optimized content that achieves the user's goals while following these strict guidelines:

    Content Structure Rules:
    1. Start with a strong hook that grabs attention
    2. Include exactly one clear call-to-action (if provided)
    3. End with relevant hashtags as specified per platform
    4. Maintain the specified brand voice throughout
    5. Adapt length based on both platform limits and user preference:
       - Short: ~25% of platform limit
       - Medium: ~50% of platform limit
       - Long: ~75% of platform limit

    Platform-Specific Formatting:
    - LinkedIn: Professional tone, business-appropriate emojis, industry hashtags
    - Twitter: Concise writing, casual tone, trending hashtags
    - Instagram: Visual language, strategic emoji use, relevant hashtags
    - Facebook: Conversational style, community focus, minimal hashtags

    IMPORTANT:
    - Return ONLY the formatted post content
    - No explanations, TextBlock wrappers, or metadata
    - Ensure all key points are naturally integrated
    - Match the specified brand voice exactly:
      * Professional: Data-driven, authoritative language
      * Casual: Friendly, approachable tone
      * Humorous: Light, entertaining style
      * Educational: Clear, informative approach
      * Inspirational: Motivating, empowering message"""

    # Enhanced user prompt with clear structure
    user_prompt = f"""Generate a {platform} post with these exact specifications:

    Platform: {platform}
    Topic: {content_topic}
    Brand Voice: {brand_voice}
    Target Audience: {target_audience}
    Length: {post_length}
    Key Points to Include: {key_points}
    Call to Action: {call_to_action if call_to_action else 'None specified'}

    Platform Constraints:
    - Character Limit: {platform_guidelines[platform]['char_limit']}
    - Style: {platform_guidelines[platform]['style']}
    - Format: {platform_guidelines[platform]['format']}
    - Hashtags: {platform_guidelines[platform]['hashtags']}"""

    # Call Claude API with optimized parameters
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.7,  # Balanced creativity while maintaining consistency
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    # Extract just the content text
    response_content = message.content[0].text if message.content else ""

    return response_content