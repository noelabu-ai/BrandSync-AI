import streamlit as st
import openai
from PIL import Image
import base64
import io
import tempfile
import os
from typing import Optional

# Set page config
st.set_page_config(
    page_title="Influencer Product Matcher",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

def encode_image_to_base64(image) -> str:
    """Convert PIL image to base64 string for OpenAI API"""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def analyze_product_influencer_match(
    product_images: list,
    product_description: str,
    video_file,
    ai_personality: str,
    api_key: str
) -> dict:
    """
    Analyze if the product matches the influencer using OpenAI
    """
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Prepare image data for API
        image_data = []
        for img in product_images:
            base64_img = encode_image_to_base64(img)
            image_data.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_img}"}
            })
        
        # Create the prompt based on personality
        personality_prompts = {
            "Professional Analyst": "As a professional brand analyst, provide a detailed assessment of product-influencer compatibility.",
            "Creative Marketer": "As a creative marketing expert, evaluate this match with innovative insights and fresh perspectives.",
            "Data-Driven Consultant": "As a data-driven consultant, analyze this match using logical frameworks and metrics.",
            "Trendy Social Media Expert": "As a trendy social media expert, assess this match from a viral content and engagement perspective.",
            "Brand Strategy Specialist": "As a brand strategy specialist, evaluate alignment between product positioning and influencer brand."
        }
        
        base_prompt = f"""
        {personality_prompts.get(ai_personality, personality_prompts['Professional Analyst'])}
        
        Analyze whether this product would be a good match for the influencer based on:
        1. Visual aesthetics and style alignment
        2. Target audience compatibility
        3. Brand values and messaging consistency
        4. Content creation potential
        5. Overall marketing synergy
        
        Product Description: {product_description}
        
        Please provide:
        - Match Score (1-10)
        - Detailed reasoning
        - Pros and cons
        - Recommendations for improvement
        - Final verdict (MATCH/NO MATCH)
        
        Note: Video analysis is simulated in this demo. In production, you would need video processing capabilities.
        """
        
        # Prepare messages for API call
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": base_prompt}
                ] + image_data
            }
        ]
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=1000
        )
        
        analysis_text = response.choices[0].message.content
        
        # Parse the response to extract match score and verdict
        match_score = 7  # Default score, you could parse this from the response
        verdict = "MATCH" if "MATCH" in analysis_text.upper() and "NO MATCH" not in analysis_text.upper() else "NO MATCH"
        
        return {
            "success": True,
            "match_score": match_score,
            "verdict": verdict,
            "analysis": analysis_text,
            "video_note": "Video analysis simulated - integrate video processing API for full functionality"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis": "Error occurred during analysis. Please check your API key and try again."
        }

# Main App UI
st.title("🎯 Influencer Product Matching App")
st.markdown("Upload your product details and influencer content to get AI-powered compatibility analysis!")

# Sidebar for API configuration
with st.sidebar:
    st.header("🔧 Configuration")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key to enable analysis"
    )
    
    st.header("🤖 AI Personality")
    ai_personality = st.selectbox(
        "Choose AI Analysis Style:",
        [
            "Professional Analyst",
            "Creative Marketer", 
            "Data-Driven Consultant",
            "Trendy Social Media Expert",
            "Brand Strategy Specialist"
        ]
    )
    
    st.markdown("---")
    st.markdown("**Note:** This demo simulates video analysis. Full video processing requires additional APIs.")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📦 Product Information")
    
    # Product images upload
    st.subheader("Product Images")
    uploaded_images = st.file_uploader(
        "Upload product images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload 1-5 high-quality product images"
    )
    
    # Display uploaded images
    if uploaded_images:
        st.write(f"✅ {len(uploaded_images)} image(s) uploaded")
        cols = st.columns(min(len(uploaded_images), 3))
        for i, img_file in enumerate(uploaded_images[:3]):
            with cols[i % 3]:
                img = Image.open(img_file)
                st.image(img, caption=f"Product {i+1}", use_column_width=True)
    
    # Product description
    st.subheader("Product Description")
    product_description = st.text_area(
        "Describe your product",
        placeholder="Enter detailed product description, target audience, key features, price range, etc.",
        height=150
    )

with col2:
    st.header("🌟 Influencer Content")
    
    # Video upload
    st.subheader("Influencer Video Sample")
    uploaded_video = st.file_uploader(
        "Upload influencer video",
        type=['mp4', 'mov', 'avi'],
        help="Upload a sample video of the influencer"
    )
    
    if uploaded_video:
        st.video(uploaded_video)
        st.success("✅ Video uploaded successfully")
    
    # Additional influencer info
    st.subheader("Additional Context (Optional)")
    influencer_context = st.text_area(
        "Influencer details",
        placeholder="Add any additional context about the influencer, their niche, audience demographics, etc.",
        height=100
    )

# Analysis section
st.markdown("---")
st.header("🔍 Analysis")

# Analysis button
if st.button("🚀 Analyze Product-Influencer Match", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not uploaded_images:
        st.error("Please upload at least one product image.")
    elif not product_description.strip():
        st.error("Please provide a product description.")
    else:
        with st.spinner("Analyzing compatibility... This may take a moment."):
            # Process uploaded images
            processed_images = []
            for img_file in uploaded_images:
                img = Image.open(img_file)
                processed_images.append(img)
            
            # Perform analysis
            result = analyze_product_influencer_match(
                processed_images,
                product_description,
                uploaded_video,
                ai_personality,
                api_key
            )
            
            st.session_state.analysis_result = result

# Display results
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    if result["success"]:
        # Create result display
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            # Match score gauge
            score = result["match_score"]
            color = "green" if score >= 7 else "orange" if score >= 5 else "red"
            st.metric("Match Score", f"{score}/10")
            
        with col2:
            # Verdict
            verdict = result["verdict"]
            if verdict == "MATCH":
                st.success(f"✅ {verdict}")
            else:
                st.error(f"❌ {verdict}")
        
        with col3:
            # AI Personality used
            st.info(f"🤖 Analysis by: {ai_personality}")
        
        # Detailed analysis
        st.subheader("📊 Detailed Analysis")
        st.write(result["analysis"])
        
        # Video note
        if "video_note" in result:
            st.info(f"📹 {result['video_note']}")
            
    else:
        st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    Built with Streamlit & OpenAI | For demo purposes
    </div>
    """,
    unsafe_allow_html=True
)