# import os
# from dotenv import load_dotenv

# # Load environment variables before importing the LangGraph application.
# load_dotenv()

# import streamlit as st
# from PIL import Image, ImageOps

# import config
# from vision_utils import analyze_skin_tone
# from agent_graph import compiled_graph

# # ============================================================
# # 1. PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="StyleSync AI | Personal Fashion Stylist",
#     page_icon="✦",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ============================================================
# # 2. SESSION STATE AND COMPLETE RESET
# # ============================================================

# if "reset_version" not in st.session_state:
#     st.session_state.reset_version = 0

# if "brand_result" not in st.session_state:
#     st.session_state.brand_result = None

# if "market_result" not in st.session_state:
#     st.session_state.market_result = None

# def clear_all_results():
#     """Clear both recommendations and recreate all form widgets."""
#     st.session_state.brand_result = None
#     st.session_state.market_result = None
#     st.session_state.reset_version += 1

# reset_version = st.session_state.reset_version

# # ============================================================
# # 3. PREMIUM FASHION UI
# # ============================================================

# st.markdown(
#     """
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');

#     :root {
#         --ivory: #faf7f1;
#         --paper: #fffdf9;
#         --burgundy: #741d36;
#         --burgundy-dark: #501225;
#         --gold: #ad8535;
#         --gold-light: #e7d7b7;
#         --ink: #30221e;
#         --muted: #786c65;
#     }

#     .stApp {
#         background: var(--ivory);
#         color: var(--ink);
#         font-family: 'DM Sans', sans-serif;
#     }

#     [data-testid="stHeader"] {
#         background: rgba(250, 247, 241, 0.96);
#     }

#     [data-testid="stMainBlockContainer"] {
#         max-width: 1450px;
#         padding-top: 1.5rem;
#         padding-bottom: 3rem;
#     }

#     h1, h2, h3 {
#         font-family: 'Playfair Display', Georgia, serif !important;
#         color: var(--ink) !important;
#     }

#     h1 {
#         font-size: clamp(2.4rem, 4vw, 4.3rem) !important;
#         line-height: 1.12 !important;
#         letter-spacing: -1.5px;
#     }

#     h2 { font-size: 2rem !important; }
#     h3 { font-size: 1.45rem !important; }

#     p, label, .stMarkdown {
#         font-family: 'DM Sans', sans-serif;
#     }

#     .brand-header {
#         display: flex;
#         align-items: center;
#         justify-content: space-between;
#         gap: 20px;
#         padding: 10px 0 22px;
#         border-bottom: 1px solid var(--gold-light);
#         margin-bottom: 28px;
#     }

#     .brand-logo {
#         color: var(--ink);
#         font-family: 'Playfair Display', Georgia, serif;
#         font-size: clamp(1.7rem, 3vw, 2.4rem);
#         font-weight: 600;
#         letter-spacing: -1px;
#     }

#     .brand-symbol {
#         color: var(--gold);
#         margin-right: 10px;
#     }

#     .brand-caption {
#         color: var(--muted);
#         font-size: 0.72rem;
#         letter-spacing: 3px;
#         text-transform: uppercase;
#         text-align: right;
#     }

#     .hero {
#         background: linear-gradient(120deg, #f4eadb, #fffaf2 68%, #ead9c3);
#         border: 1px solid #eadcc7;
#         border-radius: 22px;
#         padding: clamp(25px, 5vw, 65px);
#         margin-bottom: 28px;
#     }

#     .eyebrow {
#         color: var(--gold);
#         text-transform: uppercase;
#         letter-spacing: 3px;
#         font-size: 0.74rem;
#         font-weight: 700;
#         margin-bottom: 15px;
#     }

#     .hero-description {
#         color: var(--muted);
#         font-size: 1.08rem;
#         line-height: 1.8;
#         max-width: 720px;
#     }

#     .hero-tag {
#         display: inline-block;
#         border: 1px solid var(--gold-light);
#         border-radius: 30px;
#         padding: 8px 15px;
#         margin: 12px 5px 0 0;
#         color: var(--burgundy);
#         background: rgba(255, 255, 255, 0.55);
#         font-size: 0.82rem;
#     }

#     .section-heading {
#         color: var(--ink);
#         font-family: 'Playfair Display', Georgia, serif;
#         font-size: 1.6rem;
#         margin-bottom: 4px;
#     }

#     .section-description {
#         color: var(--muted);
#         line-height: 1.7;
#         margin-bottom: 18px;
#     }

#     .step-number {
#         color: var(--gold);
#         font-family: 'Playfair Display', Georgia, serif;
#         font-size: 1.2rem;
#         margin-right: 9px;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] {
#         background: var(--paper);
#         border: 1px solid var(--gold-light) !important;
#         border-radius: 18px !important;
#         padding: 8px;
#     }

#     [data-testid="stFileUploader"] section {
#         background: #fffcf6;
#         border: 1px dashed #cbb58f;
#         border-radius: 12px;
#     }

#     [data-testid="stFileUploader"] button {
#         border-radius: 8px;
#     }

#     [data-testid="stWidgetLabel"] p {
#         color: var(--ink);
#         font-weight: 600;
#         font-size: 0.88rem;
#     }

#     [data-baseweb="select"] > div {
#         border-radius: 9px;
#         border-color: #dfd1bf;
#         background: #fffdf9;
#     }

#     [data-testid="stSlider"] [data-baseweb="slider"] {
#         padding-top: 5px;
#     }

#     .stButton > button,
#     .stFormSubmitButton > button {
#         background: var(--burgundy);
#         color: white;
#         border: 1px solid var(--burgundy);
#         border-radius: 10px;
#         min-height: 48px;
#         padding: 0.7rem 1.2rem;
#         font-family: 'DM Sans', sans-serif;
#         font-weight: 700;
#         transition: all 0.2s ease;
#     }

#     .stButton > button:hover,
#     .stFormSubmitButton > button:hover {
#         background: var(--burgundy-dark);
#         border-color: var(--burgundy-dark);
#         color: white;
#         box-shadow: 0 5px 18px rgba(116, 29, 54, 0.18);
#     }

#     [data-testid="stTabs"] [role="tablist"] {
#         gap: 10px;
#         border-bottom: 1px solid var(--gold-light);
#     }

#     [data-testid="stTabs"] button[role="tab"] {
#         border-radius: 10px 10px 0 0;
#         padding: 13px 18px;
#         color: var(--muted);
#         font-weight: 600;
#     }

#     [data-testid="stTabs"] button[aria-selected="true"] {
#         color: var(--burgundy);
#         border-bottom: 3px solid var(--burgundy);
#     }

#     [data-testid="stAlert"] {
#         border-radius: 12px;
#     }

#     .sale-banner {
#         text-align: center;
#         background: linear-gradient(100deg, #501225, #8a2945, #501225);
#         color: white;
#         padding: 13px 16px;
#         border-radius: 12px;
#         font-size: 0.88rem;
#         margin-bottom: 24px;
#         letter-spacing: 0.3px;
#     }

#     .result-banner {
#         background: linear-gradient(120deg, #f3e7d5, #fffaf2);
#         border: 1px solid #dfc69e;
#         border-left: 5px solid #ad8535;
#         border-radius: 14px;
#         padding: 24px 28px;
#         margin: 22px 0;
#     }

#     .result-eyebrow {
#         color: #9b742c;
#         font-size: 12px;
#         font-weight: 700;
#         letter-spacing: 2.5px;
#         text-transform: uppercase;
#         margin-bottom: 8px;
#     }

#     .result-title {
#         color: #30221e;
#         font-family: 'Playfair Display', Georgia, serif;
#         font-size: clamp(25px, 3vw, 36px);
#         line-height: 1.3;
#         margin: 0 0 8px;
#     }

#     .result-subtitle {
#         color: #786c65;
#         font-size: 15px;
#         line-height: 1.8;
#         margin: 0;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h1,
#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h2,
#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h3 {
#         color: #741d36 !important;
#         line-height: 1.45 !important;
#         margin-top: 24px !important;
#         margin-bottom: 13px !important;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h1 {
#         font-size: 27px !important;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h2 {
#         font-size: 23px !important;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h3 {
#         font-size: 19px !important;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p,
#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown li {
#         color: #403630;
#         font-size: 15px;
#         line-height: 1.9;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown li {
#         margin-bottom: 7px;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown table {
#         width: 100%;
#         border-collapse: collapse;
#         font-size: 14px;
#         line-height: 1.75;
#         margin: 18px 0 25px;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown th {
#         background: #741d36 !important;
#         color: white !important;
#         text-align: left;
#         padding: 12px !important;
#         border: 1px solid #741d36 !important;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown td {
#         padding: 12px !important;
#         border: 1px solid #e6d8c5 !important;
#         vertical-align: top;
#         white-space: normal !important;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown tbody tr:nth-child(even) {
#         background: #f8f1e7;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown strong {
#         color: #501225;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown a {
#         color: #8a2945 !important;
#         font-weight: 600;
#         text-decoration: underline;
#     }

#     [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown blockquote {
#         border-left: 4px solid #ad8535;
#         background: #f8f1e7;
#         margin: 15px 0;
#         padding: 12px 18px;
#     }

#     .footer {
#         border-top: 1px solid var(--gold-light);
#         padding-top: 22px;
#         margin-top: 45px;
#         text-align: center;
#         color: var(--muted);
#         font-size: 0.8rem;
#         line-height: 1.8;
#     }

#     @media (max-width: 768px) {
#         [data-testid="stMainBlockContainer"] {
#             padding-left: 1rem;
#             padding-right: 1rem;
#         }

#         .brand-header {
#             align-items: flex-start;
#             flex-direction: column;
#         }

#         .brand-caption {
#             text-align: left;
#             letter-spacing: 1.5px;
#         }

#         .hero {
#             padding: 25px;
#         }

#         .result-banner {
#             padding: 20px;
#         }

#         [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown table {
#             font-size: 12px;
#         }

#         [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown th,
#         [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown td {
#             padding: 8px !important;
#         }
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # ============================================================
# # 4. REUSABLE HELPERS
# # ============================================================

# def prepare_image(uploaded_file):
#     """Open an uploaded image and correct its orientation."""
#     image = Image.open(uploaded_file)
#     image = ImageOps.exif_transpose(image)
#     return image.convert("RGB")

# def render_graph_trace(state, mode="brand"):
#     """Display the existing workflow and tool execution logs."""
#     if mode == "brand":
#         pipeline = (
#             "router_node → skin_analyzer_node → "
#             "brand_catalog_stylist_node"
#         )
#     else:
#         pipeline = (
#             "router_node → skin_analyzer_node → "
#             "market_fabric_tailor_node"
#         )

#     with st.expander("View LangGraph execution details", expanded=False):
#         st.markdown("**Workflow pipeline**")
#         st.code(pipeline, language="text")

#         logs = state.get("tool_execution_logs", [])

#         if logs:
#             st.markdown("**Tool execution logs**")
#             for index, log in enumerate(logs, start=1):
#                 st.write(f"{index}. {log}")
#         else:
#             st.caption(
#                 "No tool execution logs were returned for this run."
#             )

# def render_recommendation(state, heading, subtitle):
#     """Render the saved recommendation in a styled results panel."""
#     st.markdown(
#         f"""
#         <div class="result-banner">
#             <div class="result-eyebrow">
#                 STYLESYNC AI · PERSONALIZED LOOKBOOK
#             </div>
#             <div class="result-title">{heading}</div>
#             <p class="result-subtitle">{subtitle}</p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     recommendation = state.get("generated_recommendation")

#     with st.container(border=True):
#         if recommendation:
#             st.markdown(str(recommendation), unsafe_allow_html=False)
#         else:
#             st.warning(
#                 "The workflow completed, but no recommendation "
#                 "was returned. Check the graph state and node output."
#             )

#     st.caption(
#         "AI-generated recommendations. Confirm current prices, "
#         "product availability, and retailer details before purchasing."
#     )

# def analyze_uploaded_skin(uploaded_file):
#     """Analyze the uploaded skin photo and show its results."""
#     try:
#         image = prepare_image(uploaded_file)

#         st.image(
#             image,
#             caption="Your uploaded photo",
#             use_container_width=True,
#         )

#         with st.spinner("Analyzing your skin-tone palette..."):
#             skin_data = analyze_skin_tone(image)

#         st.success(
#             f"Skin tone: {skin_data.get('skin_tone', 'Not available')}"
#         )
#         st.info(
#             f"Undertone: {skin_data.get('undertone', 'Not available')}"
#         )

#         st.markdown("**Your recommended colors**")
#         st.write(skin_data.get("best_colors", "Not available"))

#         return skin_data

#     except Exception as exc:
#         st.error(
#             "Unable to analyze this image. Try a JPG or PNG image "
#             "with clear, natural lighting."
#         )
#         st.caption(f"Technical detail: {exc}")
#         return None

# # ============================================================
# # 5. BRAND HEADER AND HERO
# # ============================================================

# st.markdown(
#     """
#     <div class="brand-header">
#         <div class="brand-logo">
#             <span class="brand-symbol">✦</span> StyleSync AI
#         </div>
#         <div class="brand-caption">
#             Pakistani fashion · Personally curated
#         </div>
#     </div>

#     <div class="hero">
#         <div class="eyebrow">Your personal AI stylist</div>
#         <h1>Find the colors and silhouettes<br>
#         that feel like you.</h1>
#         <div class="hero-description">
#             Discover Pakistani fashion tailored to your skin tone,
#             body shape, personal taste and budget. From curated
#             brand collections to custom fabric styling, your next
#             favourite look starts here.
#         </div>
#         <div>
#             <span class="hero-tag">✦ Skin-tone matching</span>
#             <span class="hero-tag">✦ Pakistani brands</span>
#             <span class="hero-tag">✦ Custom tailoring</span>
#         </div>
#     </div>

#     <div class="sale-banner">
#         ✨ FESTIVE EDIT · Discover your next Pakistani fashion look
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# # ============================================================
# # 6. TWO STYLING MODES
# # ============================================================

# tab_brand, tab_market = st.tabs(
#     [
#         "✦  Brand Stylist",
#         "✂️  Custom Tailoring",
#     ]
# )

# # ============================================================
# # 7. BRAND CATALOG STYLIST
# # ============================================================

# with tab_brand:
#     st.markdown(
#         """
#         <div class="section-heading">Create your personal lookbook</div>
#         <div class="section-description">
#             Complete your color analysis and style profile to receive
#             recommendations matched to your preferences.
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     left, right = st.columns([0.95, 1.15], gap="large")

#     with left:
#         with st.container(border=True):
#             st.markdown(
#                 """
#                 <div class="section-heading">
#                     <span class="step-number">01</span>
#                     Your color palette
#                 </div>
#                 <div class="section-description">
#                     Upload a clear photo of your hand, arm or face.
#                     Your photo will be used by the existing
#                     skin-tone analysis function.
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             skin_file = st.file_uploader(
#                 "Upload your skin photo",
#                 type=["jpg", "jpeg", "png", "webp", "jfif", "heic"],
#                 key=f"brand_skin_{reset_version}",
#                 help="A clear photo in natural lighting gives the best results.",
#             )

#             skin_data = None
#             if skin_file is not None:
#                 skin_data = analyze_uploaded_skin(skin_file)

#     with right:
#         with st.container(border=True):
#             st.markdown(
#                 """
#                 <div class="section-heading">
#                     <span class="step-number">02</span>
#                     Your style profile
#                 </div>
#                 <div class="section-description">
#                     Tell us what you like. The agent will use these
#                     preferences to create a personalised lookbook.
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             gender = st.selectbox(
#                 "Gender",
#                 ["Female", "Male"],
#                 key=f"brand_gender_{reset_version}",
#             )

#             col_a, col_b = st.columns(2)

#             with col_a:
#                 age = st.slider(
#                     "Age",
#                     min_value=15,
#                     max_value=60,
#                     value=22,
#                     key=f"brand_age_{reset_version}",
#                 )

#                 height = st.selectbox(
#                     "Height range",
#                     [
#                         'Petite (Under 5\'2")',
#                         'Average (5\'2" - 5\'7")',
#                         'Tall (5\'8" and Above)',
#                     ],
#                     key=f"brand_height_{reset_version}",
#                 )

#             with col_b:
#                 if gender == "Female":
#                     body_options = [
#                         "Rectangle (Straight Silhouette)",
#                         "Hourglass (Balanced Curve)",
#                         "Pear (Narrow Shoulders, Wider Hips)",
#                         "Apple (Fuller Midsection)",
#                     ]
#                 else:
#                     body_options = [
#                         "Athletic / V-Shape (Broad Shoulders)",
#                         "Rectangle / Slim (Straight Build)",
#                         "Average / Solid (Fuller Chest & Waist)",
#                     ]

#                 body_shape = st.selectbox(
#                     "Body shape",
#                     body_options,
#                     key=f"brand_body_{gender.lower()}_{reset_version}",
#                 )

#                 selected_brand = st.selectbox(
#                     "Pakistani brand",
#                     config.PAK_BRANDS,
#                     key=f"brand_selection_{reset_version}",
#                 )

#             outfit_style = st.selectbox(
#                 "Outfit style",
#                 [
#                     "Trendy Co-ord Sets",
#                     "Long Flared Shirts & Maxis",
#                     "Short Kurti & Tulip/Straight Pants",
#                     "Classic 3-Piece Unstitched",
#                     "Modern Ready-to-Wear",
#                 ],
#                 key=f"brand_outfit_{reset_version}",
#             )

#             col_c, col_d = st.columns(2)

#             with col_c:
#                 pattern_choice = st.selectbox(
#                     "Print and pattern",
#                     [
#                         "Floral Prints (Botanical & Flower Designs)",
#                         "Geometric Prints (Sharp & Modern)",
#                         "Vertical Stripes (Height Extension)",
#                         "Minimalist Solids with Subtle Embroidery",
#                     ],
#                     key=f"brand_pattern_{reset_version}",
#                 )

#             with col_d:
#                 budget = st.selectbox(
#                     "Budget (PKR)",
#                     [
#                         "Economy (Under 4,000 PKR)",
#                         "Mid-Range (4,000 - 8,000 PKR)",
#                         "Premium (8,000 - 15,000 PKR)",
#                         "Luxury / Festive (15,000+ PKR)",
#                     ],
#                     key=f"brand_budget_{reset_version}",
#                 )

#     st.write("")

#     generate_brand = st.button(
#         "✦  Create my personalised lookbook",
#         key="btn_brand",
#         use_container_width=True,
#     )

#     if generate_brand:
#         if skin_file is None:
#             st.warning("Please upload your skin photo first.")
#         elif skin_data is None:
#             st.warning(
#                 "Skin-tone analysis did not complete. "
#                 "Please upload a supported image and try again."
#             )
#         else:
#             initial_state = {
#                 "mode": "brand_catalog",
#                 "gender": gender,
#                 "age": age,
#                 "height": height,
#                 "body_shape": body_shape,
#                 "brand": selected_brand,
#                 "outfit_style": outfit_style,
#                 "pattern_choice": pattern_choice,
#                 "budget": budget,
#                 "skin_tone": skin_data["skin_tone"],
#                 "undertone": skin_data["undertone"],
#                 "recommended_colors": skin_data["best_colors"],
#             }

#             try:
#                 with st.spinner(
#                     "Your AI stylist is curating your lookbook..."
#                 ):
#                     st.session_state.brand_result = compiled_graph.invoke(
#                         initial_state
#                     )
#             except Exception as exc:
#                 st.error(
#                     "The styling workflow could not complete. "
#                     "Check your model configuration, API limits, "
#                     "and LangGraph logs."
#                 )
#                 st.exception(exc)

#     # Show the saved result even after Streamlit reruns.
#     if st.session_state.brand_result is not None:
#         render_recommendation(
#             st.session_state.brand_result,
#             "Your curated outfit lookbook",
#             "Outfit ideas selected for your colors, silhouette, "
#             "brand, print preference and budget.",
#         )

#         render_graph_trace(st.session_state.brand_result, mode="brand")
#         st.success("Your styling recommendations are ready!")

#         st.button(
#             "↻ Reset all inputs and results",
#             key="reset_brand_all",
#             on_click=clear_all_results,
#             use_container_width=True,
#         )

# # ============================================================
# # 8. CUSTOM MARKET FABRIC STYLIST
# # ============================================================

# with tab_market:
#     st.markdown(
#         """
#         <div class="section-heading">Turn your fabric into a look</div>
#         <div class="section-description">
#             Already bought unstitched fabric? Tell us about your
#             measurements, style and event to get a tailored
#             design recommendation.
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     fabric_col, profile_col = st.columns([1, 1], gap="large")

#     with fabric_col:
#         with st.container(border=True):
#             st.markdown(
#                 """
#                 <div class="section-heading">
#                     <span class="step-number">01</span>
#                     Your fabric and colors
#                 </div>
#                 <div class="section-description">
#                     Upload your fabric and skin photos.
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             fabric_file = st.file_uploader(
#                 "Upload fabric photo",
#                 type=["jpg", "jpeg", "png", "webp", "jfif", "heic"],
#                 key=f"market_fabric_{reset_version}",
#             )

#             if fabric_file is not None:
#                 try:
#                     fabric_image = prepare_image(fabric_file)
#                     st.image(
#                         fabric_image,
#                         caption="Your fabric",
#                         use_container_width=True,
#                     )
#                 except Exception:
#                     st.error("Could not open the fabric image.")

#             market_skin_file = st.file_uploader(
#                 "Upload skin photo",
#                 type=["jpg", "jpeg", "png", "webp", "jfif", "heic"],
#                 key=f"market_skin_{reset_version}",
#             )

#             market_skin_data = None
#             if market_skin_file is not None:
#                 market_skin_data = analyze_uploaded_skin(market_skin_file)

#     with profile_col:
#         with st.container(border=True):
#             st.markdown(
#                 """
#                 <div class="section-heading">
#                     <span class="step-number">02</span>
#                     Your tailoring profile
#                 </div>
#                 <div class="section-description">
#                     Choose your preferred silhouette and occasion.
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             market_gender = st.selectbox(
#                 "Gender",
#                 ["Female", "Male"],
#                 key=f"market_gender_{reset_version}",
#             )

#             market_height = st.selectbox(
#                 "Height range",
#                 [
#                     'Petite (Under 5\'2")',
#                     'Average (5\'2" - 5\'7")',
#                     'Tall (5\'8" and Above)',
#                 ],
#                 key=f"market_height_{reset_version}",
#             )

#             if market_gender == "Female":
#                 market_body_options = [
#                     "Rectangle",
#                     "Hourglass",
#                     "Pear",
#                     "Apple",
#                 ]
#             else:
#                 market_body_options = [
#                     "Athletic / V-Shape",
#                     "Rectangle / Slim",
#                     "Average / Solid",
#                 ]

#             # FIX 1: Added gender to key to prevent invalid option error
#             market_body = st.selectbox(
#                 "Body shape",
#                 market_body_options,
#                 key=f"market_body_{market_gender.lower()}_{reset_version}",
#             )

#             desired_vibe = st.selectbox(
#                 "Event or occasion",
#                 [
#                     "Casual Everyday Wear",
#                     "Semi-Formal Dinner",
#                     "Festive / Eid Wear",
#                     "Office / University Wear",
#                 ],
#                 key=f"market_vibe_{reset_version}",
#             )

#     st.write("")

#     generate_market = st.button(
#         "✦  Design my custom outfit",
#         key="btn_market",
#         use_container_width=True,
#     )

#     if generate_market:
#         if fabric_file is None:
#             st.warning("Please upload your fabric photo first.")
#         elif market_skin_file is None:
#             st.warning("Please upload your skin photo.")
#         elif market_skin_data is None:
#             st.warning(
#                 "Skin-tone analysis failed. Please upload a "
#                 "supported image and try again."
#             )
#         else:
#             # FIX 2 & 3: Now passing recommended_colors and consistent state
#             initial_state_m = {
#                 "mode": "market_fabric",
#                 "gender": market_gender,
#                 "height": market_height,
#                 "body_shape": market_body,
#                 "desired_vibe": desired_vibe,
#                 "skin_tone": market_skin_data["skin_tone"],
#                 "undertone": market_skin_data["undertone"],
#                 "recommended_colors": market_skin_data.get("best_colors", ""),
#             }

#             try:
#                 with st.spinner(
#                     "Your AI stylist is preparing your design blueprint..."
#                 ):
#                     st.session_state.market_result = compiled_graph.invoke(
#                         initial_state_m
#                     )
#             except Exception as exc:
#                 st.error(
#                     "The tailoring workflow could not complete. "
#                     "Check your model configuration, API limits, "
#                     "and LangGraph logs."
#                 )
#                 st.exception(exc)

#     # Show the saved result even after Streamlit reruns.
#     if st.session_state.market_result is not None:
#         render_recommendation(
#             st.session_state.market_result,
#             "Your custom tailoring blueprint",
#             "A personalized design guide for your fabric, "
#             "body shape, colors and chosen occasion.",
#         )

#         render_graph_trace(st.session_state.market_result, mode="market")
#         st.success("Your tailoring recommendation is ready!")

#         st.button(
#             "↻ Reset all inputs and results",
#             key="reset_market_all",
#             on_click=clear_all_results,
#             use_container_width=True,
#         )

# # ============================================================
# # 9. FOOTER
# # ============================================================

# st.markdown(
#     """
#     <div class="footer">
#         <strong>StyleSync AI</strong><br>
#         Personalised Pakistani fashion, powered by AI.<br>
#         LangGraph · Groq · Skin-tone analysis
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

import os
from dotenv import load_dotenv

# Load environment variables BEFORE importing the LangGraph application.
load_dotenv()

import streamlit as st
from PIL import Image, ImageOps

import config
from vision_utils import analyze_skin_tone
from agent_graph import compiled_graph


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StyleSync AI | Personal Fashion Stylist",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. PREMIUM FASHION UI
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');

    :root {
        --ivory: #faf7f1;
        --paper: #fffdf9;
        --burgundy: #741d36;
        --burgundy-dark: #501225;
        --gold: #ad8535;
        --gold-light: #e7d7b7;
        --ink: #30221e;
        --muted: #786c65;
    }

    .stApp {
        background: var(--ivory);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(250, 247, 241, 0.96);
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: var(--ink) !important;
    }

    h1 {
        font-size: clamp(2.4rem, 4vw, 4.3rem) !important;
        line-height: 1.12 !important;
        letter-spacing: -1.5px;
    }

    h2 {
        font-size: 2rem !important;
    }

    h3 {
        font-size: 1.45rem !important;
    }

    p, label, .stMarkdown {
        font-family: 'DM Sans', sans-serif;
    }

    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        padding: 10px 0 22px;
        border-bottom: 1px solid var(--gold-light);
        margin-bottom: 28px;
    }

    .brand-logo {
        color: var(--ink);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(1.7rem, 3vw, 2.4rem);
        font-weight: 600;
        letter-spacing: -1px;
    }

    .brand-symbol {
        color: var(--gold);
        margin-right: 10px;
    }

    .brand-caption {
        color: var(--muted);
        font-size: 0.72rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-align: right;
    }

    .hero {
        background: linear-gradient(120deg, #f4eadb, #fffaf2 68%, #ead9c3);
        border: 1px solid #eadcc7;
        border-radius: 22px;
        padding: clamp(25px, 5vw, 65px);
        margin-bottom: 28px;
    }

    .eyebrow {
        color: var(--gold);
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.74rem;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .hero-description {
        color: var(--muted);
        font-size: 1.08rem;
        line-height: 1.8;
        max-width: 720px;
    }

    .hero-tag {
        display: inline-block;
        border: 1px solid var(--gold-light);
        border-radius: 30px;
        padding: 8px 15px;
        margin: 12px 5px 0 0;
        color: var(--burgundy);
        background: rgba(255, 255, 255, 0.55);
        font-size: 0.82rem;
    }

    .section-heading {
        color: var(--ink);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.6rem;
        margin-bottom: 4px;
    }

    .section-description {
        color: var(--muted);
        line-height: 1.7;
        margin-bottom: 18px;
    }

    .step-number {
        color: var(--gold);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.2rem;
        margin-right: 9px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--paper);
        border: 1px solid var(--gold-light) !important;
        border-radius: 18px !important;
        padding: 8px;
    }

    [data-testid="stFileUploader"] section {
        background: #fffcf6;
        border: 1px dashed #cbb58f;
        border-radius: 12px;
    }

    [data-testid="stFileUploader"] button {
        border-radius: 8px;
    }

    [data-testid="stWidgetLabel"] p {
        color: var(--ink);
        font-weight: 600;
        font-size: 0.88rem;
    }

    [data-baseweb="select"] > div {
        border-radius: 9px;
        border-color: #dfd1bf;
        background: #fffdf9;
    }

    [data-testid="stSlider"] [data-baseweb="slider"] {
        padding-top: 5px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: var(--burgundy);
        color: white;
        border: 1px solid var(--burgundy);
        border-radius: 10px;
        min-height: 48px;
        padding: 0.7rem 1.2rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: var(--burgundy-dark);
        border-color: var(--burgundy-dark);
        color: white;
        box-shadow: 0 5px 18px rgba(116, 29, 54, 0.18);
    }

    [data-testid="stTabs"] [role="tablist"] {
        gap: 10px;
        border-bottom: 1px solid var(--gold-light);
    }

    [data-testid="stTabs"] button[role="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 13px 18px;
        color: var(--muted);
        font-weight: 600;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--burgundy);
        border-bottom: 3px solid var(--burgundy);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    .sale-banner {
        text-align: center;
        background: linear-gradient(100deg, #501225, #8a2945, #501225);
        color: white;
        padding: 13px 16px;
        border-radius: 12px;
        font-size: 0.88rem;
        margin-bottom: 24px;
        letter-spacing: 0.3px;
    }

    .result-heading {
        background: #f4eadb;
        padding: 18px 22px;
        border-left: 4px solid var(--gold);
        border-radius: 5px 12px 12px 5px;
        margin: 18px 0;
    }

    .footer {
        border-top: 1px solid var(--gold-light);
        padding-top: 22px;
        margin-top: 45px;
        text-align: center;
        color: var(--muted);
        font-size: 0.8rem;
        line-height: 1.8;
    }

    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"] {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .brand-header {
            align-items: flex-start;
            flex-direction: column;
        }

        .brand-caption {
            text-align: left;
            letter-spacing: 1.5px;
        }

        .hero {
            padding: 25px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. REUSABLE HELPERS
# ============================================================

def prepare_image(uploaded_file):
    """Open an uploaded image and correct its orientation."""
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)
    return image.convert("RGB")


def render_graph_trace(state, mode="brand"):
    """Display the existing workflow and tool execution logs."""
    if mode == "brand":
        pipeline = (
            "router_node → skin_analyzer_node → "
            "brand_catalog_stylist_node"
        )
    else:
        pipeline = (
            "router_node → skin_analyzer_node → "
            "market_fabric_tailor_node"
        )

    with st.expander("View LangGraph execution details", expanded=False):
        st.markdown("**Workflow pipeline**")
        st.code(pipeline, language="text")

        logs = state.get("tool_execution_logs", [])

        if logs:
            st.markdown("**Tool execution logs**")
            for index, log in enumerate(logs, start=1):
                st.write(f"{index}. {log}")
        else:
            st.caption(
                "No tool execution logs were returned for this run."
            )


def render_recommendation(state, heading):
    """Render the recommendation returned by the existing graph."""
    st.markdown(
        f"""
        <div class="result-heading">
            <div class="eyebrow">Your personalised result</div>
            <h3>{heading}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    recommendation = state.get("generated_recommendation")

    if recommendation:
        st.markdown(str(recommendation))
    else:
        st.warning(
            "The workflow completed, but no recommendation "
            "was returned. Check the graph state and node output."
        )


def analyze_uploaded_skin(uploaded_file):
    """Analyze the uploaded skin photo and show its results."""
    try:
        image = prepare_image(uploaded_file)

        st.image(
            image,
            caption="Your uploaded photo",
            use_container_width=True,
        )

        with st.spinner("Analyzing your skin-tone palette..."):
            skin_data = analyze_skin_tone(image)

        st.success(
            f"Skin tone: {skin_data.get('skin_tone', 'Not available')}"
        )
        st.info(
            f"Undertone: {skin_data.get('undertone', 'Not available')}"
        )

        st.markdown("**Your recommended colors**")
        st.write(skin_data.get("best_colors", "Not available"))

        return skin_data

    except Exception as exc:
        st.error(
            "Unable to analyze this image. Try a JPG or PNG image "
            "with clear, natural lighting."
        )
        st.caption(f"Technical detail: {exc}")
        return None


# ============================================================
# 4. BRAND HEADER AND HERO
# ============================================================

st.markdown(
    """
    <div class="brand-header">
        <div class="brand-logo">
            <span class="brand-symbol">✦</span> StyleSync AI
        </div>
        <div class="brand-caption">
            Pakistani fashion · Personally curated
        </div>
    </div>

    <div class="hero">
        <div class="eyebrow">Your personal AI stylist</div>
        <h1>Find the colors and silhouettes<br>
        that feel like you.</h1>
        <div class="hero-description">
            Discover Pakistani fashion tailored to your skin tone,
            body shape, personal taste and budget. From curated
            brand collections to custom fabric styling, your next
            favourite look starts here.
        </div>
        <div>
            <span class="hero-tag">✦ Skin-tone matching</span>
            <span class="hero-tag">✦ Pakistani brands</span>
            <span class="hero-tag">✦ Custom tailoring</span>
        </div>
    </div>

    <div class="sale-banner">
        ✨ FESTIVE EDIT · Discover your next Pakistani fashion look
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 5. TWO STYLING MODES
# ============================================================

tab_brand, tab_market = st.tabs(
    [
        "✦  Brand Stylist",
        "✂️  Custom Tailoring",
    ]
)


# ============================================================
# 6. BRAND CATALOG STYLIST
# ============================================================

with tab_brand:
    st.markdown(
        """
        <div class="section-heading">Create your personal lookbook</div>
        <div class="section-description">
            Complete your color analysis and style profile to receive
            recommendations matched to your preferences.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([0.95, 1.15], gap="large")

    with left:
        with st.container(border=True):
            st.markdown(
                """
                <div class="section-heading">
                    <span class="step-number">01</span>
                    Your color palette
                </div>
                <div class="section-description">
                    Upload a clear photo of your hand, arm or face.
                    Your photo will be used by the existing
                    skin-tone analysis function.
                </div>
                """,
                unsafe_allow_html=True,
            )

            skin_file = st.file_uploader(
                "Upload your skin photo",
                type=["jpg", "jpeg", "png", "webp", "jfif", "heic"],
                key="brand_skin",
                help="A clear photo in natural lighting gives the best results.",
            )

            skin_data = None

            if skin_file is not None:
                skin_data = analyze_uploaded_skin(skin_file)

    with right:
        with st.container(border=True):
            st.markdown(
                """
                <div class="section-heading">
                    <span class="step-number">02</span>
                    Your style profile
                </div>
                <div class="section-description">
                    Tell us what you like. The agent will use these
                    preferences to create a personalised lookbook.
                </div>
                """,
                unsafe_allow_html=True,
            )

            gender = st.selectbox(
                "Gender",
                ["Female", "Male"],
                key="brand_gender",
            )

            col_a, col_b = st.columns(2)

            with col_a:
                age = st.slider(
                    "Age",
                    min_value=15,
                    max_value=60,
                    value=22,
                    key="brand_age",
                )

                height = st.selectbox(
                    "Height range",
                    [
                        'Petite (Under 5\'2")',
                        'Average (5\'2" - 5\'7")',
                        'Tall (5\'8" and Above)',
                    ],
                    key="brand_height",
                )

            with col_b:
                if gender == "Female":
                    body_options = [
                        "Rectangle (Straight Silhouette)",
                        "Hourglass (Balanced Curve)",
                        "Pear (Narrow Shoulders, Wider Hips)",
                        "Apple (Fuller Midsection)",
                    ]
                else:
                    body_options = [
                        "Athletic / V-Shape (Broad Shoulders)",
                        "Rectangle / Slim (Straight Build)",
                        "Average / Solid (Fuller Chest & Waist)",
                    ]

                body_shape = st.selectbox(
                    "Body shape",
                    body_options,
                    key=f"brand_body_{gender.lower()}",
                )

                selected_brand = st.selectbox(
                    "Pakistani brand",
                    config.PAK_BRANDS,
                    key="brand_selection",
                )

            outfit_style = st.selectbox(
                "Outfit style",
                [
                    "Trendy Co-ord Sets",
                    "Long Flared Shirts & Maxis",
                    "Short Kurti & Tulip/Straight Pants",
                    "Classic 3-Piece Unstitched",
                    "Modern Ready-to-Wear",
                ],
                key="brand_outfit",
            )

            col_c, col_d = st.columns(2)

            with col_c:
                pattern_choice = st.selectbox(
                    "Print and pattern",
                    [
                        "Floral Prints (Botanical & Flower Designs)",
                        "Geometric Prints (Sharp & Modern)",
                        "Vertical Stripes (Height Extension)",
                        "Minimalist Solids with Subtle Embroidery",
                    ],
                    key="brand_pattern",
                )

            with col_d:
                budget = st.selectbox(
                    "Budget (PKR)",
                    [
                        "Economy (Under 4,000 PKR)",
                        "Mid-Range (4,000 - 8,000 PKR)",
                        "Premium (8,000 - 15,000 PKR)",
                        "Luxury / Festive (15,000+ PKR)",
                    ],
                    key="brand_budget",
                )

    st.write("")

    generate_brand = st.button(
        "✦  Create my personalised lookbook",
        key="btn_brand",
        use_container_width=True,
    )

    if generate_brand:
        if skin_file is None:
            st.warning("Please upload your skin photo first.")
        elif skin_data is None:
            st.warning(
                "Skin-tone analysis did not complete. "
                "Please upload a supported image and try again."
            )
        else:
            initial_state = {
                "mode": "brand_catalog",
                "gender": gender,
                "age": age,
                "height": height,
                "body_shape": body_shape,
                "brand": selected_brand,
                "outfit_style": outfit_style,
                "pattern_choice": pattern_choice,
                "budget": budget,
                "skin_tone": skin_data["skin_tone"],
                "undertone": skin_data["undertone"],
                "recommended_colors": skin_data["best_colors"],
            }

            try:
                with st.spinner(
                    "Your AI stylist is curating your lookbook..."
                ):
                    final_state = compiled_graph.invoke(initial_state)

                st.divider()
                  
                render_recommendation(
                final_state,
                "Your curated outfit lookbook",
                 )

                render_graph_trace(final_state, mode="brand")

                st.success("Your styling recommendations are ready!")

                if st.button("✕ Clear Results", key="clear_brand_results"):
                   st.rerun()
 
                # render_recommendation(
                #     final_state,
                #     "Your curated outfit lookbook",
                # )

                # render_graph_trace(final_state, mode="brand")

                # st.success("Your styling recommendations are ready!")

            except Exception as exc:
                st.error(
                    "The styling workflow could not complete. "
                    "Check your model configuration, API limits, "
                    "and LangGraph logs."
                )
                st.exception(exc)


# ============================================================
# 7. CUSTOM MARKET FABRIC STYLIST
# ============================================================

with tab_market:
    st.markdown(
        """
        <div class="section-heading">Turn your fabric into a look</div>
        <div class="section-description">
            Already bought unstitched fabric? Tell us about your
            measurements, style and event to get a tailored
            design recommendation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    fabric_col, profile_col = st.columns([1, 1], gap="large")

    with fabric_col:
        with st.container(border=True):
            st.markdown(
                """
                <div class="section-heading">
                    <span class="step-number">01</span>
                    Your fabric and colors
                </div>
                <div class="section-description">
                    Upload your fabric and skin photos.
                </div>
                """,
                unsafe_allow_html=True,
            )

            fabric_file = st.file_uploader(
                "Upload fabric photo",
                type=["jpg", "jpeg", "png", "webp", "jfif", "heic"],
                key="market_fabric",
            )

            if fabric_file is not None:
                try:
                    fabric_image = prepare_image(fabric_file)
                    st.image(
                        fabric_image,
                        caption="Your fabric",
                        use_container_width=True,
                    )
                except Exception:
                    st.error("Could not open the fabric image.")

            market_skin_file = st.file_uploader(
                "Upload skin photo",
                type=["jpg", "jpeg", "png", "webp", "jfif", "heic"],
                key="market_skin",
            )

            market_skin_data = None

            if market_skin_file is not None:
                market_skin_data = analyze_uploaded_skin(
                    market_skin_file
                )

    with profile_col:
        with st.container(border=True):
            st.markdown(
                """
                <div class="section-heading">
                    <span class="step-number">02</span>
                    Your tailoring profile
                </div>
                <div class="section-description">
                    Choose your preferred silhouette and occasion.
                </div>
                """,
                unsafe_allow_html=True,
            )

            market_gender = st.selectbox(
                "Gender",
                ["Female", "Male"],
                key="market_gender",
            )

            market_height = st.selectbox(
                "Height range",
                [
                    'Petite (Under 5\'2")',
                    'Average (5\'2" - 5\'7")',
                    'Tall (5\'8" and Above)',
                ],
                key="market_height",
            )

            if market_gender == "Female":
                market_body_options = [
                    "Rectangle",
                    "Hourglass",
                    "Pear",
                    "Apple",
                ]
            else:
                market_body_options = [
                    "Athletic / V-Shape",
                    "Rectangle / Slim",
                    "Average / Solid",
                ]

            market_body = st.selectbox(
                "Body shape",
                market_body_options,
                key="market_body",
            )

            desired_vibe = st.selectbox(
                "Event or occasion",
                [
                    "Casual Everyday Wear",
                    "Semi-Formal Dinner",
                    "Festive / Eid Wear",
                    "Office / University Wear",
                ],
                key="market_vibe",
            )

    st.write("")

    generate_market = st.button(
        "✦  Design my custom outfit",
        key="btn_market",
        use_container_width=True,
    )

    if generate_market:
        if fabric_file is None:
            st.warning("Please upload your fabric photo first.")
        elif market_skin_file is None:
            st.warning("Please upload your skin photo.")
        elif market_skin_data is None:
            st.warning(
                "Skin-tone analysis failed. Please upload a "
                "supported image and try again."
            )
        else:
            initial_state_m = {
                "mode": "market_fabric",
                "gender": market_gender,
                "height": market_height,
                "body_shape": market_body,
                "desired_vibe": desired_vibe,
                "skin_tone": market_skin_data["skin_tone"],
                "undertone": market_skin_data["undertone"],
            }

            try:
                with st.spinner(
                    "Your AI stylist is preparing your design blueprint..."
                ):
                    final_state_m = compiled_graph.invoke(
                        initial_state_m
                    )

                st.divider()

                # render_recommendation(
                #     final_state_m,
                #     "Your custom tailoring blueprint",
                # )

                # render_graph_trace(final_state_m, mode="market")

                # st.success("Your tailoring recommendation is ready!")

                
                render_recommendation(
                   final_state_m,
                   "Your custom tailoring blueprint",
               )
               
                render_graph_trace(final_state_m, mode="market")
               
                st.success("Your tailoring recommendation is ready!")
               
                if st.button("✕ Clear Results", key="clear_market_results"):
                   st.rerun()


            except Exception as exc:
                st.error(
                    "The tailoring workflow could not complete. "
                    "Check your model configuration, API limits, "
                    "and LangGraph logs."
                )
                st.exception(exc)


# ============================================================
# 8. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <strong>StyleSync AI</strong><br>
        Personalised Pakistani fashion, powered by AI.<br>
        LangGraph · Groq · Skin-tone analysis
    </div>
    """,
    unsafe_allow_html=True,
)