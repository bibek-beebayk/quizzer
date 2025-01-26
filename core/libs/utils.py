def calculate_reading_time(content, words_per_minute=250):
    """
    Calculate estimated reading time for a blog post.
    
    Args:
        content (str): Blog post content
        words_per_minute (int, optional): Average reading speed. Defaults to 250.
    
    Returns:
        int: Estimated reading time in minutes
    """
    # Remove HTML tags if present
    import re
    content = re.sub(r'<[^>]+>', '', content)
    
    # Count words
    word_count = len(content.split())
    
    # Calculate reading time
    reading_time = max(1, word_count // words_per_minute)
    
    return reading_time