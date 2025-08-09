import openai
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class OpenAIChains:
    def __init__(self):
        """Initialize OpenAI client with API key from environment variables"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            st.error("OpenAI API key not found! Please add it to your .env file")
            st.stop()
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"  # or "gpt-3.5-turbo" or "gpt-4o-mini"
    
    def generate_titles(self, topic):
        """Generate blog title suggestions based on topic"""
        try:
            prompt = f"""
            Generate 5 creative and engaging blog titles for the topic: "{topic}"
            
            Requirements:
            - Titles should be catchy and SEO-friendly
            - Each title should be on a new line
            - Titles should be between 40-70 characters
            - Make them appealing to readers
            - Avoid clickbait but make them interesting
            
            Format: Return only the titles, one per line, no numbering or bullets.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert content creator and SEO specialist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Error generating titles: {str(e)}")
            return f"The Ultimate Guide to {topic}\nUnderstanding {topic}: A Complete Overview\nHow {topic} is Transforming Our World\nEverything You Need to Know About {topic}\nThe Future of {topic}: Trends and Insights"
    
    def generate_title_suggestions(self, topic):
        """Generate multiple title suggestions for AI title generation feature"""
        try:
            prompt = f"""
            Generate 8 creative and diverse blog title suggestions for the topic: "{topic}"
            
            Requirements:
            - Create titles with different angles and approaches
            - Mix of question-based, how-to, list-based, and declarative titles
            - Titles should be SEO-friendly and engaging
            - Each title should be between 40-70 characters
            - Make them click-worthy but not clickbait
            - Include emotional triggers where appropriate
            
            Categories to include:
            1. How-to guide
            2. Question-based
            3. List/number-based
            4. Ultimate guide
            5. Trend/future focused
            6. Problem-solution
            7. Beginner's guide
            8. Expert insights
            
            Format: Return only the titles, one per line, no numbering or bullets.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert content strategist and SEO specialist who creates compelling blog titles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.8
            )
            
            titles = response.choices[0].message.content.strip().split('\n')
            return [title.strip() for title in titles if title.strip()]
            
        except Exception as e:
            st.error(f"Error generating title suggestions: {str(e)}")
            return [
                f"The Complete Guide to {topic}",
                f"How to Master {topic}: A Step-by-Step Guide",
                f"Why {topic} Matters in 2024",
                f"10 Essential Tips for {topic}",
                f"Understanding {topic}: Everything You Need to Know",
                f"The Future of {topic}: Trends and Predictions",
                f"Common {topic} Mistakes and How to Avoid Them",
                f"Beginner's Guide to {topic}"
            ]
    
    def generate_blog(self, title, keywords="", blog_length=1000, tone="informative", seo_optimized=False):
        """Generate blog content based on title, keywords, length, tone, and SEO optimization"""
        try:
            word_target = blog_length
            
            # Tone-specific instructions
            tone_instructions = {
                "formal": "Use professional language, avoid contractions, maintain academic tone, use sophisticated vocabulary.",
                "casual": "Use conversational language, include contractions, write like talking to a friend, use simple vocabulary.",
                "informative": "Focus on providing facts and information, use clear explanations, include educational content.",
                "persuasive": "Use compelling arguments, include call-to-actions, focus on convincing the reader.",
                "friendly": "Use warm and approachable language, include personal touches, make it welcoming.",
                "professional": "Use business-appropriate language, maintain authority, focus on expertise and credibility.",
                "humorous": "Include light humor where appropriate, use engaging and entertaining language, keep it fun.",
                "technical": "Use industry-specific terminology, include detailed explanations, focus on technical accuracy."
            }
            
            tone_instruction = tone_instructions.get(tone.lower(), tone_instructions["informative"])
            
            # SEO optimization instructions
            seo_instruction = ""
            if seo_optimized:
                seo_instruction = """
                
                SEO OPTIMIZATION REQUIREMENTS:
                - Include the main keyword in the title, first paragraph, and throughout the content naturally
                - Use header tags (H2, H3) with relevant keywords
                - Include meta-description worthy content in the introduction
                - Add internal linking suggestions where relevant
                - Use LSI keywords and related terms
                - Optimize for featured snippets with clear, concise answers
                - Include a table of contents structure
                - Use bullet points and numbered lists for better readability
                - Aim for keyword density of 1-2% for main keywords
                """
            
            prompt = f"""
            Write a comprehensive blog post with the following specifications:
            
            Title: "{title}"
            Target Length: {word_target} words
            Keywords to include: {keywords if keywords else "None specified"}
            Tone: {tone} - {tone_instruction}
            {seo_instruction}
            
            Requirements:
            - Write an engaging introduction that hooks the reader
            - Create well-structured content with clear headings and subheadings
            - Include relevant examples and insights
            - Maintain the specified tone throughout: {tone}
            - Ensure the content is informative and valuable
            - If keywords are provided, naturally incorporate them throughout the content
            - Conclude with a strong summary or call-to-action
            - Use markdown formatting for headers (##, ###)
            
            Structure:
            1. Engaging introduction (hook the reader)
            2. Main content sections with subheadings
            3. Practical examples or case studies where relevant
            4. Conclusion with key takeaways
            
            Write the complete blog post now with the {tone} tone:
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are an expert content writer who creates high-quality, engaging blog posts. You excel at writing in different tones and styles, and you understand SEO best practices."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=min(4000, word_target * 2),
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Error generating blog content: {str(e)}")
            return f"""
            # {title}
            
            ## Introduction
            
            We apologize, but there was an error generating your blog content. This could be due to:
            - API rate limits
            - Network connectivity issues
            - Invalid API key
            - Model availability issues
            
            Please check your OpenAI API key and try again.
            
            ## Troubleshooting
            
            1. Verify your API key in the .env file
            2. Check your OpenAI account has sufficient credits
            3. Ensure you have internet connectivity
            4. Try using a different model (gpt-3.5-turbo or gpt-4o-mini)
            
            **Keywords requested:** {keywords}
            **Target length:** {blog_length} words
            **Tone:** {tone}
            **SEO Optimized:** {seo_optimized}
            """

    def generate_blog_direct(self, topic, tone="informative", seo_optimized=False, blog_length=1000):
        """Generate blog content directly from topic without title selection"""
        try:
            # Generate a title first
            title_response = self.generate_titles(topic)
            titles = [title.strip() for title in title_response.split('\n') if title.strip()]
            selected_title = titles[0] if titles else f"Complete Guide to {topic}"
            
            # Generate blog content
            return self.generate_blog(
                title=selected_title,
                keywords=topic,
                blog_length=blog_length,
                tone=tone,
                seo_optimized=seo_optimized
            )
            
        except Exception as e:
            st.error(f"Error in direct blog generation: {str(e)}")
            return f"Error generating blog for topic: {topic}"

    def regenerate_blog_with_suggestions(self, title, keywords="", blog_length=1000, suggestions="", original_content="", tone="informative", seo_optimized=False):
        """Regenerate blog content based on user suggestions and feedback"""
        try:
            word_target = blog_length
            
            # Tone-specific instructions
            tone_instructions = {
                "formal": "Use professional language, avoid contractions, maintain academic tone.",
                "casual": "Use conversational language, include contractions, write like talking to a friend.",
                "informative": "Focus on providing facts and information, use clear explanations.",
                "persuasive": "Use compelling arguments, include call-to-actions.",
                "friendly": "Use warm and approachable language, include personal touches.",
                "professional": "Use business-appropriate language, maintain authority.",
                "humorous": "Include light humor where appropriate, keep it engaging.",
                "technical": "Use industry-specific terminology, include detailed explanations."
            }
            
            tone_instruction = tone_instructions.get(tone.lower(), tone_instructions["informative"])
            
            seo_instruction = ""
            if seo_optimized:
                seo_instruction = "Also ensure the content is SEO optimized with proper keyword usage, header structure, and readability."
            
            prompt = f"""
            I need you to improve and regenerate a blog post based on specific user feedback and suggestions.
            
            ORIGINAL BLOG DETAILS:
            Title: "{title}"
            Target Length: {word_target} words
            Keywords: {keywords if keywords else "None specified"}
            Tone: {tone} - {tone_instruction}
            SEO Optimized: {seo_optimized}
            
            USER SUGGESTIONS FOR IMPROVEMENT:
            {suggestions}
            
            ORIGINAL CONTENT TO IMPROVE:
            {original_content[:1000]}...  
            
            TASK:
            Please rewrite the entire blog post from scratch, incorporating all the user suggestions while maintaining the original title and requirements. 
            
            SPECIFIC REQUIREMENTS:
            - Address ALL the user suggestions mentioned above
            - Keep the same title: "{title}"
            - Target length: {word_target} words
            - Include keywords: {keywords if keywords else "relevant keywords"}
            - Maintain the {tone} tone throughout
            - Make the content significantly different and improved
            - Use markdown formatting for headers (##, ###)
            - Ensure the new version is engaging and high-quality
            {seo_instruction}
            
            IMPROVEMENT FOCUS:
            - If user wants more engagement: Add stories, questions, interactive elements
            - If user wants more examples: Include practical cases, statistics, real-world applications
            - If user wants more detail: Expand explanations, add depth and comprehensive coverage
            - If user wants tone changes: Adjust writing style accordingly (but maintain the selected {tone} tone)
            - If user wants better structure: Reorganize content flow and headings
            - If user wants more professionalism: Make content more authoritative
            
            Generate the complete improved blog post now with the {tone} tone:
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are an expert content writer who excels at improving content based on specific user feedback. You create high-quality, engaging blog posts that address user concerns and suggestions perfectly while maintaining the specified tone."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=min(4000, word_target * 2),
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Error regenerating blog content: {str(e)}")
            return f"""
            # {title}
            
            ## Error During Regeneration
            
            We encountered an error while regenerating your blog content based on your suggestions.
            
            **Your Suggestions Were:**
            {suggestions}
            
            **Error Details:**
            - {str(e)}
            
            **Please try again with:**
            1. Shorter or more specific suggestions
            2. Check your API quota and connectivity
            3. Try again in a few moments
            
            **Original Parameters:**
            - Title: {title}
            - Keywords: {keywords}
            - Target Length: {blog_length} words
            - Tone: {tone}
            - SEO Optimized: {seo_optimized}
            """

# Global variable to store the AI chains instance
_ai_chains_instance = None

def get_ai_chains():
    """Get AI chains instance with error handling and caching"""
    global _ai_chains_instance
    
    if _ai_chains_instance is None:
        try:
            _ai_chains_instance = OpenAIChains()
        except Exception as e:
            st.error(f"Failed to initialize AI chains: {str(e)}")
            return None
    
    return _ai_chains_instance

def initialize_ai_chains():
    """Initialize AI chains with comprehensive error handling"""
    global _ai_chains_instance
    
    try:
        # Check if API key exists
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            st.error("❌ OpenAI API key not found!")
            st.markdown("""
            ### 🔧 Setup Instructions:
            1. Create a `.env` file in your project directory
            2. Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`
            3. Restart the application
            """)
            return None
        
        # Try to create the instance
        _ai_chains_instance = OpenAIChains()
        
        # Test the connection with a simple request
        try:
            test_response = _ai_chains_instance.client.chat.completions.create(
                model=_ai_chains_instance.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            st.success(f"✅ AI service connected successfully! Using model: {_ai_chains_instance.model}")
            return _ai_chains_instance
            
        except Exception as api_error:
            st.error(f"❌ API connection failed: {str(api_error)}")
            
            # Provide specific error guidance
            if "model" in str(api_error).lower():
                st.warning("⚠️ Model not available. Trying alternative model...")
                _ai_chains_instance.model = "gpt-3.5-turbo"
                try:
                    test_response = _ai_chains_instance.client.chat.completions.create(
                        model=_ai_chains_instance.model,
                        messages=[{"role": "user", "content": "Hello"}],
                        max_tokens=5
                    )
                    st.success(f"✅ Connected with fallback model: {_ai_chains_instance.model}")
                    return _ai_chains_instance
                except:
                    st.error("❌ No available models found")
                    _ai_chains_instance = None
                    return None
            
            elif "rate_limit" in str(api_error).lower():
                st.error("❌ Rate limit exceeded. Please wait and try again.")
                _ai_chains_instance = None
                return None
            
            elif "insufficient_quota" in str(api_error).lower():
                st.error("❌ Insufficient API quota. Please check your OpenAI billing.")
                _ai_chains_instance = None
                return None
            
            else:
                st.error("❌ Unknown API error. Please check your configuration.")
                _ai_chains_instance = None
                return None
                
    except Exception as e:
        st.error(f"Failed to initialize AI chains: {str(e)}")
        _ai_chains_instance = None
        return None

def check_api_status():
    """Check if the API is working correctly"""
    chains = get_ai_chains()
    if not chains:
        return False, "AI chains not initialized"
    
    try:
        response = chains.client.chat.completions.create(
            model=chains.model,
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=1
        )
        return True, f"API working with model: {chains.model}"
    except Exception as e:
        return False, f"API error: {str(e)}"

def reset_ai_chains():
    """Reset the AI chains instance (useful for troubleshooting)"""
    global _ai_chains_instance
    _ai_chains_instance = None
    return initialize_ai_chains()