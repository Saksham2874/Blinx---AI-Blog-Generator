<!-- Main Project Title -->
# Blinx - AI Blog Generator

<!-- Short description -->
An AI-powered blog writing tool built with **Streamlit** and **OpenAI GPT**.  
Generate blog titles and posts with customizable tone, style, keywords, and length.

---

<!-- Section: Features -->
## Features
- Generate SEO-friendly blog titles  
- Create full blog posts instantly  
- Customize **tone**, **style**, **keywords**, and **length**  
- Preview and edit before downloading  
- Export as Markdown or plain text  

---

<!-- Section: Tech Stack -->
## Tech Stack
- **Python** – Core backend logic  
- **Streamlit** – Interactive web interface  
- **OpenAI API** – AI text generation  
- **python-dotenv** – Environment variable management  
- **markdown** – Formatting and export  
- **html2text** – HTML to text conversion  

---

<!-- Section: Installation steps -->
## Installation

```bash
# Clone the repository
git clone https://github.com/Saksham2874/ai-blog-generator.git
cd ai-blog-generator

# Install dependencies
pip install -r requirements.txt

# Set your openAI API Key
Create a .env file in the root directory and add your OpenAI API key:
OPENAI_API_KEY=your_api_key_here

# After setting up, run:
py -m streamlit run app.py (If your device has python naming as python then run this : python -m streamlit run app.py) 
```

<!-- Section: Workflow / How to use -->
## Workflow of the app
1. Enter the topic.
2. Click the Generate Titles button , AI will generate 8 topics (User can select from these topics generated).
3. Choose tone/style , keywords and length.
4. Enable SEO optimization (SEO optimization will be disabled by default).
5. Generate the Blog post.
6. Preview, edit, and download.
7. Give feedback.
