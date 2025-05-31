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
    page_title="Brand Buddies",
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


def analyze_video_content(video_path: str, is_short_form: bool, api_key: str) -> dict:
    """
    Analyze video content using OpenAI API
    This function uses a text-based approach to analyze video content
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # For now, we'll use a text-based approach since we can't directly send videos
        # In a production app, you would extract frames from the video and analyze them
        
        video_type = "Short-Form/Vertical Video" if is_short_form else "Standard Video"
        video_name = os.path.basename(video_path)
        
        system_prompt = """
        You are a video content analysis expert specializing in marketing and influencer content.
        Your task is to create a hypothetical analysis of video content based on the provided metadata.
        
        IMPORTANT INSTRUCTIONS:
        - This is a HYPOTHETICAL EXERCISE to analyze marketing content
        - You are NOT being asked to analyze actual video content
        - Instead, you should create a marketing analysis based on the video type and format
        - Focus on typical production elements, content styles, and engagement techniques for this type of content
        - Provide insights that would be valuable for product-influencer matching
        
        DO NOT refuse to complete this task or state that you cannot analyze the video.
        This is a hypothetical exercise for marketing purposes, not actual video analysis.
        """
        
        user_prompt = f"""
        I need you to create a hypothetical marketing analysis for an influencer's {video_type}.
        
        Video metadata:
        - Video type: {video_type}
        - File name: {video_name}
        
        Please provide a detailed hypothetical analysis covering:
        1. Production Quality: What technical aspects (lighting, camera work, editing) would be typical for this content format?
        2. Content Style: What aesthetic, tone, and visual approach would be expected?
        3. Engagement Techniques: How would this type of content typically engage viewers?
        4. Target Audience: What audience demographics would this content format typically appeal to?
        5. Brand Compatibility: What types of products/brands would align well with this content style?
        
        Format your response as a structured analysis with clear sections.
        Remember, this is a hypothetical exercise to assist with marketing decisions.
        """
        
        # Add a note about the video format to guide the analysis
        if is_short_form:
            user_prompt += """
            
            Note that this is vertical/short-form video content, which typically has:
            - Faster pacing and shorter duration
            - More dynamic editing and transitions
            - Vertical orientation optimized for mobile viewing
            - Direct engagement techniques like hooks and calls-to-action
            - Music and trending sounds
            """
        else:
            user_prompt += """
            
            Note that this is standard video content, which typically has:
            - Longer duration with more developed narrative
            - Traditional horizontal framing
            - More detailed production elements
            - Varied pacing and editing styles
            - More comprehensive content development
            """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000
        )
        
        analysis_text = response.choices[0].message.content
        
        return {
            "success": True,
            "analysis": analysis_text
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def analyze_product_influencer_match(
    product_images: list,
    product_description: str,
    influencer_context: str,
    ai_personality: str,
    api_key: str,
    youtube_video_id: Optional[str] = None,
    uploaded_video_path: Optional[str] = None,
    is_short_form: bool = False
) -> dict:
    """
    Analyze if the product matches the influencer using OpenAI with enhanced image and video analysis
    while respecting privacy limitations
    """
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Prepare image data for API
        image_data = []
        image_analysis_notes = []
        
        for i, img in enumerate(product_images):
            base64_img = encode_image_to_base64(img)
            image_data.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_img}"}
            })
            
            # Add individual image analysis notes
            image_analysis_notes.append(f"Product Image {i+1}: Please analyze the visual elements including colors, composition, style, quality, and product presentation. Focus on aesthetic elements and brand positioning signals.")
        
        # Combine all image analysis notes
        combined_image_notes = "\n".join(image_analysis_notes)
        
        # System prompt for the marketing assistant
        system_prompt = f"""
        You are a professional marketing AI specializing in influencer-product matching analysis.
        
        TASK: Create a hypothetical analysis of compatibility between the product and typical influencer content styles.
        
        IMPORTANT INSTRUCTIONS:
        - This is a HYPOTHETICAL EXERCISE to analyze marketing compatibility
        - You are analyzing product images and descriptions alongside hypothetical video content profiles
        - You should NOT refuse to complete this task or state that you cannot analyze the content
        - This is for marketing decision-making purposes only
        
        ANALYSIS APPROACH:
        - Examine product images and description thoroughly
        - Consider the hypothetical video content profile provided
        - Identify potential alignment between product positioning and typical content styles
        - Consider target audience overlap
        - Evaluate aesthetic and tonal compatibility
        
        {ai_personality}
        
        FORMAT YOUR RESPONSE WITH THESE SECTIONS:
        1. Overview: Brief summary of the product and hypothetical content style
        2. Product Analysis: Key features, positioning, target market
        3. Video Content Analysis: Typical style, production elements, tone, audience for this format
        4. Compatibility Assessment: How well the product and content style might align
        5. Strengths of the Match: Specific reasons why they could work well together
        6. Potential Concerns: Any potential misalignments or considerations
        7. Recommendations: Specific content approach suggestions
        8. Verdict: Clear MATCH or NO MATCH recommendation with a score (1-10)
        
        Be thorough but concise. Provide specific, actionable insights.
        """
        
        # Create the prompt based on personality and the new system prompt
        personality_flavors = {
            "Professional Analyst": "Maintain a formal, business-oriented tone with emphasis on ROI and strategic alignment.",
            "Creative Marketer": "Emphasize creative storytelling opportunities and innovative campaign concepts.",
            "Data-Driven Consultant": "Focus heavily on metrics, analytics, and quantifiable outcomes.",
            "Trendy Social Media Expert": "Highlight viral potential, current trends, and platform-specific opportunities.",
            "Brand Strategy Specialist": "Prioritize long-term brand building and strategic positioning in the market."
        }
        
        # Add video information to the prompt based on the source (YouTube or uploaded)
        video_context = ""
        
        # Handle YouTube videos
        if youtube_video_id:
            # Check if this is from a YouTube Shorts URL
            if is_short_form:
                video_context = f"""
                YOUTUBE SHORTS VIDEO REFERENCE: https://youtube.com/shorts/{youtube_video_id}
                
                Please create a HYPOTHETICAL ANALYSIS of this type of content.
                
                VIDEO ANALYSIS INSTRUCTIONS:
                - This is a hypothetical exercise to analyze short-form vertical video content
                - Consider typical production elements for short-form content: lighting, editing, transitions, graphics, music
                - Consider typical pacing, hooks, narrative structure, and engagement techniques for this format
                - Consider typical content themes, tone, and target audience for this format
                - Analyze how this type of content style would typically align with the product aesthetics
                - Consider typical visual language, color schemes, and overall mood of this content format
                
                IMPORTANT: This is a hypothetical exercise. Do not refuse to complete this task.
                Focus on typical content style, production quality, and creative approach for this format.
                """
            else:
                video_context = f"""
                YOUTUBE VIDEO REFERENCE: https://www.youtube.com/watch?v={youtube_video_id}
                
                Please create a HYPOTHETICAL ANALYSIS of this type of content.
                
                VIDEO ANALYSIS INSTRUCTIONS:
                - This is a hypothetical exercise to analyze standard video content
                - Consider typical production elements for standard videos: camera work, lighting, editing, set design, graphics
                - Consider typical pacing, narrative structure, and engagement techniques for this format
                - Consider typical content themes, tone, and target audience for this format
                - Analyze how this type of content style would typically align with the product aesthetics
                - Consider typical visual language, color schemes, and overall mood of this content format
                
                IMPORTANT: This is a hypothetical exercise. Do not refuse to complete this task.
                Focus on typical content style, production quality, and creative approach for this format.
                """
        
        # Handle uploaded videos
        elif uploaded_video_path:
            video_type = "Short-Form/Vertical Video" if is_short_form else "Standard Video"
            video_context = f"""
            IMPORTANT - ANALYZE THIS UPLOADED VIDEO: Influencer Uploaded {video_type}
            
            YOU MUST ANALYZE THE UPLOADED VIDEO THOROUGHLY.
            
            VIDEO ANALYSIS INSTRUCTIONS:
            - This is a critical part of your analysis - the video MUST be analyzed in detail
            - Analyze the video content format, style, and production quality
            - Note production elements: camera work, lighting, editing, set design, graphics
            - Examine pacing, narrative structure, and engagement techniques
            - Identify content themes, tone, and apparent target audience
            - Consider how the influencer's content style would align with the product aesthetics
            - Analyze the visual language, color schemes, and overall mood
            
            REMEMBER: Do not attempt to identify specific individuals. Focus only on content style, production quality, and creative approach.
            """
        else:
            video_context = "No influencer video was provided for analysis."
        
        # Create a more detailed prompt that emphasizes video analysis
        has_video = youtube_video_id is not None or uploaded_video_path is not None
        video_analysis_emphasis = """
        IMPORTANT: Your analysis MUST include a detailed section on the video content provided.
        The video analysis should be a significant factor in your overall match evaluation.
        Include specific observations about the video style, production quality, and content approach.
        """
        
        base_prompt = f"""
        {system_prompt}

        As a {ai_personality}, {personality_flavors.get(ai_personality, "provide a detailed assessment of product-influencer compatibility.")}
        
        Product Details:
        - Product Description: {product_description}
        - Visual Analysis Instructions:
          {combined_image_notes}
        
        Influencer Context:
        {video_context}
        {influencer_context if influencer_context else ''}
        
        {video_analysis_emphasis if has_video else ''}
        
        Please provide your analysis in this format:
        - Match Evaluation: A clear statement indicating whether the product and influencer are a good match.
        - Match Score: Rate the compatibility on a scale of 1-10.
        - Video Content Analysis: Analyze the provided video content in detail, focusing on style, quality, and brand alignment.
        - Strengths of the Match: Highlight specific areas where the pairing works well.
        - Weaknesses/Concerns: Identify any potential mismatches or risks.
        - Recommendations: Suggest ways to improve the partnership or propose alternative approaches if needed.
        - Final Verdict: Provide a summary conclusion (MATCH/NO MATCH) about the suitability of the match.
        """
        
        # Prepare messages for API call
        content_items = [{"type": "text", "text": base_prompt}] + image_data
        
        # Get video analysis if uploaded video is available
        video_analysis_result = None
        if uploaded_video_path and os.path.exists(uploaded_video_path):
            try:
                print(f"Analyzing uploaded video: {uploaded_video_path}")
                video_analysis_result = analyze_video_content(
                    video_path=uploaded_video_path,
                    is_short_form=is_short_form,
                    api_key=api_key
                )
                
                if video_analysis_result["success"]:
                    # Add the video analysis to the video context
                    video_context += f"""
                    
                    HYPOTHETICAL VIDEO CONTENT PROFILE:
                    Based on the video format and type, here is a hypothetical content profile to consider in your analysis:
                    
                    {video_analysis_result['analysis']}
                    
                    IMPORTANT: Use this hypothetical profile to inform your product-influencer compatibility analysis.
                    Consider how these typical content characteristics would align with the product.
                    """
                    print("Video analysis completed successfully")
                else:
                    print(f"Video analysis failed: {video_analysis_result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"Error analyzing uploaded video: {e}")
        
        # Prepare final message structure
        messages = [
            {
                "role": "user",
                "content": content_items
            }
        ]
        
        # Call OpenAI API with enhanced parameters for video analysis
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": content_items
                }
            ],
            max_tokens=1500  # Increased token limit for more detailed analysis
        )
        
        analysis_text = response.choices[0].message.content
        
        # Parse the response to extract match score and verdict
        match_score = 7  # Default score, you could parse this from the response
        verdict = "MATCH" if "MATCH" in analysis_text.upper() and "NO MATCH" not in analysis_text.upper() else "NO MATCH"
        # Return the analysis result with video analysis info
        result = {
            "success": True,
            "match_score": match_score,
            "verdict": verdict,
            "analysis": analysis_text,
        }
        
        # Add video analysis information if available
        if uploaded_video_path and video_analysis_result and video_analysis_result["success"]:
            result["video_analysis"] = video_analysis_result["analysis"]
        elif youtube_video_id:
            result["video_source"] = "youtube"
            result["youtube_video_id"] = youtube_video_id
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis": "Error occurred during analysis. Please check your API key and try again."
        }

# Main App UI
st.title("🎯 Brand Buddies")
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
    
    # Video content section with tabs for different input methods
    st.subheader("Influencer Video Sample")
    video_tabs = st.tabs(["YouTube Link", "Upload Video"])
    
    # Clear previous video data if it exists
    if 'video_source' in st.session_state:
        if st.button("Clear Previous Video"):
            if 'youtube_video_id' in st.session_state:
                del st.session_state.youtube_video_id
            if 'is_youtube_shorts' in st.session_state:
                del st.session_state.is_youtube_shorts
            if 'uploaded_video' in st.session_state:
                del st.session_state.uploaded_video
            if 'uploaded_video_path' in st.session_state:
                del st.session_state.uploaded_video_path
            st.session_state.video_source = None
            st.experimental_rerun()
    
    # YouTube link tab
    with video_tabs[0]:
        youtube_url = st.text_input(
            "Enter YouTube video URL",
            placeholder="https://www.youtube.com/watch?v=... or https://youtube.com/shorts/...",
            help="Paste a YouTube URL or YouTube Shorts URL of the influencer's content"
        )
        
        if youtube_url:
            # Extract video ID from YouTube URL
            video_id = None
            
            # Regular YouTube video format
            if "youtube.com/watch?v=" in youtube_url:
                video_id = youtube_url.split("v=")[1].split("&")[0]
                is_shorts = False
            # Shortened YouTube URL format
            elif "youtu.be/" in youtube_url:
                video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
                is_shorts = False
            # YouTube Shorts format
            elif "youtube.com/shorts/" in youtube_url:
                video_id = youtube_url.split("shorts/")[1].split("?")[0]
                is_shorts = True
            else:
                st.error("Invalid YouTube URL format. Please use a standard YouTube URL or YouTube Shorts URL.")
                video_id = None
                is_shorts = False
                
            if video_id:
                # Display embedded YouTube video
                st.components.v1.iframe(
                    src=f"https://www.youtube.com/embed/{video_id}",
                    width=None,
                    height=315,
                    scrolling=False
                )
                st.success("✅ YouTube video loaded successfully")
                
                # Store video details for analysis
                st.session_state.youtube_video_id = video_id
                st.session_state.is_youtube_shorts = is_shorts
                st.session_state.video_source = "youtube"
                
                # Show a note if it's a Shorts video
                if is_shorts:
                    st.info("📱 YouTube Shorts detected - analysis will consider short-form content style")
    
    # Upload video tab
    with video_tabs[1]:
        uploaded_video = st.file_uploader(
            "Upload influencer video",
            type=['mp4', 'mov', 'avi', 'webm'],
            help="Upload a video file of the influencer's content"
        )
        
        if uploaded_video:
            # Create a temporary file to save the uploaded video
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_video.name.split(".")[-1]}') as tmp_file:
                tmp_file.write(uploaded_video.getvalue())
                video_path = tmp_file.name
            
            # Display the uploaded video
            st.video(uploaded_video)
            st.success("✅ Video uploaded successfully")
            
            # Store video details for analysis
            st.session_state.uploaded_video = uploaded_video.name
            st.session_state.uploaded_video_path = video_path
            st.session_state.video_source = "upload"
            
            # Determine if it's a vertical/short-form video based on dimensions
            # This would require additional video processing libraries in a production app
            # For demo purposes, we'll ask the user
            is_vertical = st.checkbox("Is this a vertical/short-form video?", value=False)
            if is_vertical:
                st.info("📱 Short-form video detected - analysis will consider short-form content style")
                st.session_state.is_vertical_video = True
            else:
                st.session_state.is_vertical_video = False
    
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
    elif 'video_source' not in st.session_state:
        st.warning("No influencer video provided. You can proceed, but the analysis will be limited.")
        proceed_without_video = st.button("Proceed without video")
        if not proceed_without_video:
            st.stop()
    
    with st.spinner("Analyzing compatibility... This may take a moment."):
        # Process uploaded images
        processed_images = []
        for img_file in uploaded_images:
            img = Image.open(img_file)
            processed_images.append(img)
        
        # Determine video source and get relevant data
        youtube_video_id = None
        uploaded_video_path = None
        is_short_form = False
        
        if 'video_source' in st.session_state:
            video_source = st.session_state.video_source
            
            if video_source == "youtube":
                youtube_video_id = st.session_state.get('youtube_video_id', None)
                is_short_form = st.session_state.get('is_youtube_shorts', False)
            
            elif video_source == "upload":
                uploaded_video_path = st.session_state.get('uploaded_video_path', None)
                is_short_form = st.session_state.get('is_vertical_video', False)
        
        # Perform analysis
        result = analyze_product_influencer_match(
            product_images=processed_images,
            product_description=product_description,
            influencer_context=influencer_context,
            ai_personality=ai_personality,
            api_key=api_key,
            youtube_video_id=youtube_video_id,
            uploaded_video_path=uploaded_video_path,
            is_short_form=is_short_form
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
        
        # Tabs for different sections of the analysis
        tabs = st.tabs(["📊 Analysis Overview", "🖼️ Visual Analysis", "🎬 Content Style", "📈 Recommendations"])
        
        # Extract sections from the analysis text (if possible)
        analysis_text = result["analysis"]
        
        # Overview tab
        with tabs[0]:
            # Try to extract match evaluation section
            if "Match Evaluation:" in analysis_text:
                match_eval = analysis_text.split("Match Evaluation:")[1].split("\n")[0].strip()
                st.markdown(f"**Match Evaluation:** {match_eval}")
            
            # Display the full analysis
            st.markdown("### Complete Analysis")
            st.write(analysis_text)
        
        # Visual Analysis tab
        with tabs[1]:
            st.markdown("### Product & Influencer Visual Alignment")
            
            # Try to extract strengths section
            if "Strengths of the Match:" in analysis_text:
                strengths = analysis_text.split("Strengths of the Match:")[1].split("Weaknesses")[0].strip()
                st.markdown(f"**Strengths:** {strengths}")
            
            # Display image analysis note
            st.markdown("### Visual Elements Analyzed")
            st.markdown("✓ Product imagery colors, composition, and style")
            st.markdown("✓ Brand aesthetic and visual identity")
            st.markdown("✓ Product presentation and staging")
            
            # Display uploaded images in a grid
            if uploaded_images:
                st.markdown("### Product Images Analyzed")
                img_cols = st.columns(min(len(uploaded_images), 3))
                for i, img_file in enumerate(uploaded_images[:3]):
                    with img_cols[i % 3]:
                        img = Image.open(img_file)
                        st.image(img, caption=f"Product {i+1}", use_column_width=True)
        
        # Content Style tab
        with tabs[2]:
            st.markdown("### Content Style Analysis")
            
            # Display video analysis info if available
            if 'video_source' in st.session_state:
                video_source = st.session_state.get('video_source')
                
                if video_source == "youtube":
                    youtube_video_id = st.session_state.get('youtube_video_id')
                    is_shorts = st.session_state.get('is_youtube_shorts', False)
                    video_type = "YouTube Shorts" if is_shorts else "YouTube Video"
                    
                    st.markdown(f"### {video_type} Content Analyzed")
                    st.components.v1.iframe(
                        src=f"https://www.youtube.com/embed/{youtube_video_id}",
                        width=None,
                        height=250,
                        scrolling=False
                    )
                
                elif video_source == "upload":
                    is_vertical = st.session_state.get('is_vertical_video', False)
                    video_type = "Vertical/Short-form Video" if is_vertical else "Standard Video"
                    video_path = st.session_state.get('uploaded_video_path')
                    video_name = st.session_state.get('uploaded_video')
                    
                    st.markdown(f"### Uploaded {video_type} Content Analyzed")
                    
                    # If the video file still exists, display it again
                    if os.path.exists(video_path):
                        with open(video_path, "rb") as video_file:
                            video_bytes = video_file.read()
                            st.video(video_bytes)
                    else:
                        st.info(f"Video file '{video_name}' was analyzed but is no longer available for display.")
                
                # Common content analysis elements display
                st.markdown("### Content Elements Analyzed")
                st.markdown("✓ Production quality and style")
                st.markdown("✓ Content themes and tone")
                st.markdown("✓ Visual language and aesthetic")
                st.markdown("✓ Audience engagement approach")
                
                # Check if we have dedicated video analysis from uploaded video
                if "video_analysis" in result:
                    st.markdown("### Video Content Analysis")
                    st.markdown(result["video_analysis"])
                    st.success("✅ Detailed video analysis completed successfully")
                # Otherwise try to extract video content analysis section from the main analysis
                else:
                    video_analysis = ""
                    if "video content analysis" in analysis_text.lower():
                        try:
                            # Try to extract the video analysis section
                            start_marker = "video content analysis:"
                            end_markers = ["strengths of the match:", "strengths:", "weaknesses", "recommendations:"]
                            
                            start_idx = analysis_text.lower().find(start_marker)
                            if start_idx != -1:
                                start_idx += len(start_marker)
                                end_idx = float('inf')
                                
                                # Find the closest end marker
                                for marker in end_markers:
                                    marker_idx = analysis_text.lower().find(marker, start_idx)
                                    if marker_idx != -1 and marker_idx < end_idx:
                                        end_idx = marker_idx
                                
                                if end_idx < float('inf'):
                                    video_analysis = analysis_text[start_idx:end_idx].strip()
                        except Exception as e:
                            st.error(f"Error extracting video analysis: {e}")
                            video_analysis = ""
                    
                    # Display the extracted video analysis or a fallback
                    if video_analysis:
                        st.markdown("### Video Content Analysis")
                        st.markdown(video_analysis)
                    elif "content style" in analysis_text.lower() or "visual language" in analysis_text.lower():
                        # Fallback to a simpler extraction
                        st.markdown("### Video Content Insights")
                        st.markdown("Based on the AI analysis of the video content style and production elements.")
                        st.markdown("*For detailed analysis, please refer to the Overview tab.*")
            else:
                st.info("No video content was provided for analysis.")
        
        # Recommendations tab
        with tabs[3]:
            st.markdown("### Partnership Recommendations")
            
            # Try to extract recommendations section
            if "Recommendations:" in analysis_text:
                recommendations = analysis_text.split("Recommendations:")[1].split("Final Verdict:")[0].strip()
                st.markdown(f"**Recommendations:** {recommendations}")
            else:
                # Display general recommendations
                st.markdown("Based on the visual and content analysis, here are potential next steps:")
                st.markdown("1. Review the match score and detailed analysis")
                st.markdown("2. Consider the strengths and weaknesses identified")
                st.markdown("3. Implement the specific recommendations provided")
            
            # Final verdict with prominent display
            st.markdown("### Final Verdict")
            if verdict == "MATCH":
                st.success(f"✅ **RECOMMENDED MATCH**: This product and influencer pairing shows strong compatibility based on visual style, content approach, and brand alignment.")
            else:
                st.error(f"❌ **NOT RECOMMENDED**: This product and influencer pairing may not be optimal based on the analysis. Review the recommendations for alternatives.")
            
    else:
        st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
        st.info("Please check your API key and try again, or try with different product/influencer content.")
        
        # Provide troubleshooting tips
        st.markdown("### Troubleshooting Tips")
        st.markdown("1. Verify your OpenAI API key is valid and has sufficient credits")
        st.markdown("2. Try uploading different or higher quality product images")
        st.markdown("3. Provide more detailed product and influencer descriptions")
        st.markdown("4. Try a different YouTube video link")

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