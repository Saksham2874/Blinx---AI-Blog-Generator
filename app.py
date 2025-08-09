import streamlit as st
import time
from ai_chains import get_ai_chains

# Page configuration
st.set_page_config(
    page_title="Blinx",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """

    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 0.6rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.12);
        padding: 0.5rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.3rem;
        margin-bottom: 2.5rem;
        font-style: italic;
    }
    
    .section-header {
        color: #2E86AB;
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2E86AB;
        padding-bottom: 0.5rem;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .preview-area {
        background: #1e1e1e !important;
        border: 2px dashed #2E86AB;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        min-height: 200px;
        color: white !important;
    }

    .edit-area {
        background: #2a2a2a !important;
        border: 2px dashed #2E86AB;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        min-height: 200px;
        color: white !important;
    }

    .preview-area p, .preview-area li, .preview-area span, 
    .preview-area div, .preview-area strong, .preview-area em {
        color: white !important;
    }

    .preview-area blockquote {
        border-left: 4px solid #2E86AB;
        padding-left: 1rem;
        margin: 1rem 0;
        font-style: italic;
        color: white !important;
    }

    .api-status {
        background: #2e2e2e !important;
        border: 1px solid #2E86AB;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: white !important;
    }

    .title-suggestion-box {
        background: #2e2e2e !important;
        border: 1px solid #2E86AB;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s;
        color: white !important;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #222 !important;
        border: 1px solid #2E86AB !important;
        color: white !important;
    }

    .stMarkdown {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Initialize AI chains
@st.cache_resource
def initialize_ai():
    """Initialize AI chains and cache the instance"""
    return get_ai_chains()

# Header section
st.markdown('<div class="main-header">Blinx : AI Blog Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Create Blogs using GenAI</div>', unsafe_allow_html=True)

# Check API status
ai_chains = initialize_ai()
if ai_chains is None:
    st.markdown('<div class="warning-box">⚠️ AI service not available. Please check your OpenAI API key in the .env file.</div>', unsafe_allow_html=True)
    st.stop()
else:
    st.markdown('<div class="api-status">✅ AI service connected successfully!</div>', unsafe_allow_html=True)

# Initialize session state for all features
if 'blog_topic' not in st.session_state:
    st.session_state['blog_topic'] = ""
if 'selected_tone' not in st.session_state:
    st.session_state['selected_tone'] = "informative"
if 'seo_optimized' not in st.session_state:
    st.session_state['seo_optimized'] = False
if 'generated_content' not in st.session_state:
    st.session_state['generated_content'] = ""
if 'is_editing' not in st.session_state:
    st.session_state['is_editing'] = False
if 'edited_content' not in st.session_state:
    st.session_state['edited_content'] = ""
if 'user_feedback' not in st.session_state:
    st.session_state['user_feedback'] = ""
if 'feedback_rating' not in st.session_state:
    st.session_state['feedback_rating'] = 5
if 'blog_length' not in st.session_state:
    st.session_state['blog_length'] = 1000
if 'title_suggestions' not in st.session_state:
    st.session_state['title_suggestions'] = []
if 'selected_title' not in st.session_state:
    st.session_state['selected_title'] = ""
if 'show_title_generator' not in st.session_state:
    st.session_state['show_title_generator'] = False

# Sidebar for settings and tips
with st.sidebar:
    st.markdown("### Blog Settings")
    
    # Blog length setting
    st.session_state['blog_length'] = st.slider(
        " Blog Length (words)",
        min_value=100,
        max_value=3000,
        value=st.session_state['blog_length'],
        step=50,
        help="Choose the desired length of your blog post"
    )
    
    st.markdown("###  Quick Tips")
    st.markdown("""
    For Best Results:
    - Use specific, clear topics
    - Choose appropriate tone for your audience
    - Enable SEO optimization for better reach
    - Use AI title generator for better titles
    - Review and edit the generated content
    - Provide detailed feedback for improvements
    """)
    
    st.markdown("### 📊 Generation Stats")
    if st.session_state.get('generated_content'):
        word_count = len(st.session_state['generated_content'].split())
        st.metric("Words Generated", word_count)
        st.metric("Target Words", st.session_state['blog_length'])
        accuracy = min(100, (word_count / st.session_state['blog_length']) * 100)
        st.metric("Length Accuracy", f"{accuracy:.1f}%")

# Main content area - Feature 1: Topic Input Field
st.markdown('<div class="section-header"> Topic Input</div>', unsafe_allow_html=True)
#st.markdown('<div class="feature-box">', unsafe_allow_html=True)
st.markdown(" What would you like to write about?")

topic_input = st.text_input(
    "Enter your blog topic:",
    placeholder=" ",
    key="topic_input",
    help="Be specific about your topic for better content generation",
    value=st.session_state['blog_topic']
)

if topic_input != st.session_state['blog_topic']:
    st.session_state['blog_topic'] = topic_input

st.markdown('</div>', unsafe_allow_html=True)

# NEW FEATURE: AI Title Generation
if st.session_state['blog_topic']:
    st.markdown('<div class="section-header">🤖 AI Title Generator</div>', unsafe_allow_html=True)
    
    col_title1, col_title2 = st.columns([2, 1])
    
    with col_title1:
        st.markdown("Generate AI-powered title suggestions for your blog:")
    
    with col_title2:
        if st.button("Generate Titles", key="generate_titles_btn"):
            with st.spinner(' Generating creative titles...'):
                try:
                    title_suggestions = ai_chains.generate_title_suggestions(st.session_state['blog_topic'])
                    st.session_state['title_suggestions'] = title_suggestions
                    st.session_state['show_title_generator'] = True
                    st.success(f"✨ Generated {len(title_suggestions)} title suggestions!")
                except Exception as e:
                    st.error(f"Error generating titles: {str(e)}")
    
    # Display title suggestions if available
    if st.session_state.get('title_suggestions') and st.session_state['show_title_generator']:
        st.markdown(" ✨ AI Generated Title Suggestions:")
        st.markdown("*Click on any title to select it for your blog post*")
        
        # Display titles in a grid
        for i, title in enumerate(st.session_state['title_suggestions']):
            if st.button(f" {title}", key=f"title_select_{i}", help="Click to select this title"):
                st.session_state['selected_title'] = title
                st.success(f"✅ Selected title: {title}")
                st.rerun()
        
        # Show selected title
        if st.session_state.get('selected_title'):
            st.markdown(f" Selected Title: {st.session_state['selected_title']}")

# Feature 2: Tone Selection Dropdown
st.markdown('<div class="section-header"> Tone Selection</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    #st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown(" Choose your writing tone:")
    
    tone_options = {
        "informative": " Informative - Educational and factual",
        "casual": " Casual - Friendly and conversational", 
        "formal": " Formal - Professional and academic",
        "persuasive": " Persuasive - Compelling and convincing",
        "friendly": " Friendly - Warm and approachable",
        "professional": " Professional - Business-oriented",
        "humorous": " Humorous - Light and entertaining",
        "technical": " Technical - Detailed and specialized"
    }
    
    selected_tone = st.selectbox(
        "Select tone:",
        options=list(tone_options.keys()),
        format_func=lambda x: tone_options[x],
        index=list(tone_options.keys()).index(st.session_state['selected_tone']),
        help="Choose the tone that best fits your target audience"
    )
    
    st.session_state['selected_tone'] = selected_tone
    st.markdown('</div>', unsafe_allow_html=True)

# Feature 4: SEO Optimization Checkbox
with col2:
    #st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown(" SEO Optimization:")
    
    seo_enabled = st.checkbox(
        "✅ Enable SEO Optimization",
        value=st.session_state['seo_optimized'],
        help="Optimize content for search engines with better keyword usage, headers, and structure"
    )
    
    st.session_state['seo_optimized'] = seo_enabled
    
    if seo_enabled:
        st.markdown("SEO Features:")
        st.markdown("• Keyword optimization")
        st.markdown("• Header structure")
        st.markdown("• Meta-description content")
        st.markdown("• Readability improvements")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Feature 3: Generate Button
st.markdown('<div class="section-header"> Content Generation</div>', unsafe_allow_html=True)

if st.session_state['blog_topic']:
    st.markdown(f"Topic: {st.session_state['blog_topic']}")
    if st.session_state.get('selected_title'):
        st.markdown(f"Selected Title: {st.session_state['selected_title']}")
    st.markdown(f"Tone: {tone_options[st.session_state['selected_tone']]}")
    st.markdown(f"SEO Optimized: {'✅ Yes' if st.session_state['seo_optimized'] else '❌ No'}")
    st.markdown(f"Target Length: {st.session_state['blog_length']} words")
    
    col_gen1, col_gen2, col_gen3 = st.columns([1, 1, 2])
    
    with col_gen1:
        generate_blog_btn = st.button(
            " Generate Blog Post",
            key="generate_blog_main",
            help="Generate your blog post with the selected settings"
        )
    
    if generate_blog_btn:
        with st.spinner('🤖 AI is crafting your blog post... This may take a moment.'):
            try:
                # Use selected title if available, otherwise generate from topic
                if st.session_state.get('selected_title'):
                    # Generate blog content with selected title
                    blog_content = ai_chains.generate_blog(
                        title=st.session_state['selected_title'],
                        keywords=st.session_state['blog_topic'],
                        blog_length=st.session_state['blog_length'],
                        tone=st.session_state['selected_tone'],
                        seo_optimized=st.session_state['seo_optimized']
                    )
                else:
                    # Generate blog content directly from topic
                    blog_content = ai_chains.generate_blog_direct(
                        topic=st.session_state['blog_topic'],
                        tone=st.session_state['selected_tone'],
                        seo_optimized=st.session_state['seo_optimized'],
                        blog_length=st.session_state['blog_length']
                    )
                
                st.session_state['generated_content'] = blog_content
                st.session_state['edited_content'] = blog_content  # Initialize edited content
                
                st.success("Blog post generated successfully!")
                
            except Exception as e:
                st.error(f"Error generating blog: {str(e)}")
else:
    st.markdown('<div class="info-box"> Please enter a topic above to generate your blog post</div>', unsafe_allow_html=True)

# Feature 5: Preview Area
if st.session_state.get('generated_content'):
    st.markdown('<div class="section-header"> Preview Area</div>', unsafe_allow_html=True)
    
    # Tab-based preview and edit interface
    preview_tab, edit_tab = st.tabs([" Preview", " Edit & Save"])
    
    with preview_tab:
        #st.markdown('<div class="preview-area">', unsafe_allow_html=True)
        st.markdown("###  Generated Blog Preview")
        
        # Display the content (either original or edited)
        content_to_show = st.session_state.get('edited_content', st.session_state['generated_content'])
        st.markdown(content_to_show)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download options
        col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 2])
        
        with col_dl1:
            # Create safe filename
            safe_topic = "".join(c for c in st.session_state['blog_topic'] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_topic = safe_topic.replace(' ', '_')[:30]
            filename = f"blog_{safe_topic}.md"
            
            st.download_button(
                label=" Download as Markdown",
                data=content_to_show,
                file_name=filename,
                mime="text/markdown",
                help="Download your blog post as a Markdown file"
            )
        
        with col_dl2:
            # Download as plain text
            txt_filename = f"blog_{safe_topic}.txt"
            st.download_button(
                label=" Download as Text",
                data=content_to_show,
                file_name=txt_filename,
                mime="text/plain",
                help="Download your blog post as a plain text file"
            )
    
    # Feature 6: Edit and Save Options
    with edit_tab:
        #st.markdown('<div class="edit-area">', unsafe_allow_html=True)
        st.markdown("### Edit Your Blog Post")
        
        # Text area for editing
        edited_content = st.text_area(
            "Edit your blog content:",
            value=st.session_state.get('edited_content', st.session_state['generated_content']),
            height=400,
            help="Make any changes you want to the generated content"
        )
        
        col_edit1, col_edit2, col_edit3 = st.columns([1, 1, 2])
        
        with col_edit1:
            if st.button(" Save Changes", key="save_changes"):
                st.session_state['edited_content'] = edited_content
                st.success("✅ Changes saved successfully!")
                st.rerun()
        
        with col_edit2:
            if st.button(" Reset to Original", key="reset_content"):
                st.session_state['edited_content'] = st.session_state['generated_content']
                st.info(" Content reset to original version")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Real-time word count for edited content
        if edited_content:
            word_count = len(edited_content.split())
            st.metric("Current Word Count", word_count)

# Feature 7: User Feedback Section
if st.session_state.get('generated_content'):
    st.markdown('<div class="section-header"> User Feedback</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
    st.markdown("### How was the generated content?")
    st.markdown("Your feedback helps us improve the AI blog generator!")
    
    # Rating system
    col_rating1, col_rating2 = st.columns([1, 2])
    
    with col_rating1:
        feedback_rating = st.slider(
            " Rate the generated content:",
            min_value=1,
            max_value=5,
            value=st.session_state['feedback_rating'],
            help="1 = Poor, 5 = Excellent"
        )
        st.session_state['feedback_rating'] = feedback_rating
        
        # Display rating with stars
        stars = "⭐" * feedback_rating + "☆" * (5 - feedback_rating)
        st.markdown(f"Your Rating: {stars}")
    
    with col_rating2:
        # Quick feedback buttons
        st.markdown("Quick Feedback:")
        col_fb1, col_fb2, col_fb3 = st.columns(3)
        
        with col_fb1:
            if st.button("👍 Excellent!", key="fb_excellent"):
                st.session_state['user_feedback'] += "Content was excellent! "
                st.success("Thank you for the positive feedback!")
        
        with col_fb2:
            if st.button("👌 Good", key="fb_good"):
                st.session_state['user_feedback'] += "Content was good overall. "
                st.success("Thanks for your feedback!")
        
        with col_fb3:
            if st.button("👎 Needs Work", key="fb_needs_work"):
                st.session_state['user_feedback'] += "Content needs improvement. "
                
    
    
    # Submit feedback
    col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 2])
    
    with col_submit1:
        if st.button("Submit Feedback", key="submit_feedback"):
            # Compile comprehensive feedback
            compiled_feedback = f"""
            Rating: {feedback_rating}/5 stars
            
            Blog Settings:
            - Topic: {st.session_state['blog_topic']}
            - Tone: {st.session_state['selected_tone']}
            - SEO Enabled: {st.session_state['seo_optimized']}
            - Target Length: {st.session_state['blog_length']} words
            """
            
            # Store feedback (in a real app, this would go to a database)
            st.session_state['compiled_feedback'] = compiled_feedback
            
            st.success(" Thank you for your feedback! It will help improve the Blinx App.")
            
    
    with col_submit2:
        if st.button(" Regenerate with Feedback", key="regenerate_with_feedback"):
            if st.session_state['user_feedback'].strip():
                with st.spinner('Regenerating content based on your feedback...'):
                    try:
                        # Use selected title or generate one from topic
                        title_to_use = st.session_state.get('selected_title', f"Blog about {st.session_state['blog_topic']}")
                        
                        # Use feedback to regenerate content
                        improved_content = ai_chains.regenerate_blog_with_suggestions(
                            title=title_to_use,
                            keywords=st.session_state['blog_topic'],
                            blog_length=st.session_state['blog_length'],
                            suggestions=st.session_state['user_feedback'],
                            original_content=st.session_state['generated_content'],
                            tone=st.session_state['selected_tone'],
                            seo_optimized=st.session_state['seo_optimized']
                        )
                        
                        st.session_state['generated_content'] = improved_content
                        st.session_state['edited_content'] = improved_content
                        
                        st.success("Content regenerated based on your feedback!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error regenerating content: {str(e)}")
            else:
                st.warning("Please provide some feedback before regenerating!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Advanced Features Section
if st.session_state.get('generated_content'):
    st.markdown('<div class="section-header">Advanced Features</div>', unsafe_allow_html=True)
    
    col_adv1, col_adv2 = st.columns(2)
    
    with col_adv1:
        with st.expander("Content Analytics"):
            content_to_analyze = st.session_state.get('edited_content', st.session_state['generated_content'])
            
            # Basic analytics
            word_count = len(content_to_analyze.split())
            char_count = len(content_to_analyze)
            paragraph_count = len([p for p in content_to_analyze.split('\n\n') if p.strip()])
            
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric(" Words", word_count)
                st.metric(" Characters", char_count)
            
            with col_metric2:
                st.metric(" Paragraphs", paragraph_count)
                reading_time = max(1, word_count // 200)  # Assume 200 words per minute
                st.metric(" Reading Time", f"{reading_time} min")
            
            # Content analysis
            if st.button("Analyze Content", key="analyze_content"):
                st.markdown("Content Analysis:")
                
                # Count headers
                headers = [line for line in content_to_analyze.split('\n') if line.startswith('#')]
                st.markdown(f"• Headers: {len(headers)}")
                
                # Check for questions
                questions = content_to_analyze.count('?')
                st.markdown(f"• Questions: {questions}")
                
                # Check for lists
                lists = content_to_analyze.count('•') + content_to_analyze.count('-')
                st.markdown(f"• List items: {lists}")
                
                # Topic keyword density
                topic_mentions = content_to_analyze.lower().count(st.session_state['blog_topic'].lower())
                density = (topic_mentions / word_count) * 100 if word_count > 0 else 0
                st.markdown(f"• Topic keyword density: {density:.1f}%")
    
    with col_adv2:
        with st.expander(" SEO Insights"):
            if st.session_state['seo_optimized']:
                st.markdown("SEO Analysis:")
                
                content = st.session_state.get('edited_content', st.session_state['generated_content'])
                
                # Check for SEO elements
                has_h1 = '# ' in content
                has_h2 = '## ' in content
                has_h3 = '### ' in content
                
                st.markdown(f"• H1 Headers: {'✅' if has_h1 else '❌'}")
                st.markdown(f"• H2 Headers: {'✅' if has_h2 else '❌'}")
                st.markdown(f"• H3 Headers: {'✅' if has_h3 else '❌'}")
                
                # Word count check for SEO
                word_count = len(content.split())
                if word_count >= 300:
                    st.markdown(f"• Word Count: ✅ {word_count} words (Good for SEO)")
                else:
                    st.markdown(f"• Word Count: ⚠️ {word_count} words (Consider adding more)")
                
                # Check for topic in first paragraph
                first_paragraph = content.split('\n\n')[0] if '\n\n' in content else content[:200]
                topic_in_intro = st.session_state['blog_topic'].lower() in first_paragraph.lower()
                st.markdown(f"• Topic in intro: {'✅' if topic_in_intro else '❌'}")
                
            else:
                st.info("Enable SEO optimization to see SEO insights!")

