import typing_extensions as typing
from typing import TypedDict, Optional, List, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
import config
import urllib.parse

# ==============================================================================
# 1. DEFINE LANGCHAIN TOOLS (Tool Calling Architecture)
# ==============================================================================

@tool
def search_brand_catalog(brand_name: str, pattern_keyword: str, outfit_style: str) -> str:
    """
    Generates an exact direct filtered product search URL for Pakistani clothing brands 
    including Khaadi, Sapphire, Gul Ahmed, Ethnic, Cross Stitch, and Junaid Jamshed.
    """
    brand_search_urls = {
        "Khaadi": "https://pk.khaadi.com/search?q=",
        "Sapphire": "https://pk.sapphireonline.pk/search?q=",
        "Gul Ahmed": "https://www.gulahmedshop.com/catalogsearch/result/?q=",
        "Junaid Jamshed (J.)": "https://www.junaidjamshed.com/catalogsearch/result/?q=",
        "Ethnic": "https://pk.ethnc.com/pages/search-results-page?q=",
        "Cross Stitch": "https://crossstitch.pk/pages/search-results-page?q=",
        "Limelight": "https://www.limelight.pk/pages/search-results-page?q=",
        "Bonanza Satrangi": "https://www.bonanzasatrangi.com/search?q=",
        "Sana Safinaz": "https://www.sanasafinaz.com/pk/catalogsearch/result/?q=",
        "Alkaram Studio": "https://www.alkaramstudio.com/search?q=",
        "Outfitters": "https://www.outfitters.com.pk/search?q="
    }
    
    clean_pattern = pattern_keyword.split('(')[0].strip()
    search_query = f"{clean_pattern} {outfit_style}".strip()
    encoded_query = urllib.parse.quote(search_query)
    
    base_url = brand_search_urls.get(brand_name, "https://pk.khaadi.com/search?q=")
    return f"{base_url}{encoded_query}"


@tool
def fetch_footwear_accessories_links(skin_tone: str) -> dict:
    """
    Generates direct search links for matching footwear brands (Stylo and Borjan) 
    tailored to the user's skin tone profile.
    """
    stylo_link = f"https://www.stylo.pk/search?q={urllib.parse.quote(skin_tone + ' sandals')}"
    borjan_link = f"https://www.borjan.com.pk/search?q={urllib.parse.quote('khussa shoes')}"
    return {
        "stylo_footwear": stylo_link,
        "borjan_khussa": borjan_link
    }


# Register tools in a list for LLM binding
tools = [search_brand_catalog, fetch_footwear_accessories_links]


# ==============================================================================
# 2. DEFINE LANGGRAPH STATE
# ==============================================================================
class AgentState(TypedDict):
    mode: str                    # "brand_catalog" or "market_fabric"
    gender: str
    height: str
    body_shape: str
    skin_tone: str
    undertone: str
    recommended_colors: str
    
    # Mode-Specific Inputs
    brand: Optional[str]
    outfit_style: Optional[str]
    pattern_choice: Optional[str]
    budget: Optional[str]
    desired_vibe: Optional[str]
    
    # Outputs & Tool Results
    exact_filtered_link: Optional[str]
    tool_execution_logs: List[str]
    generated_recommendation: Optional[str]
    execution_status: str


# ==============================================================================
# 3. LANGGRAPH NODES WITH TOOL CALLING
# ==============================================================================

def router_node(state: AgentState) -> AgentState:
    state["execution_status"] = "Routing request through LangGraph workflow..."
    state["tool_execution_logs"] = []
    return state

def skin_analyzer_node(state: AgentState) -> AgentState:
    if not state.get("skin_tone"):
        state["skin_tone"] = "Medium / Wheatish"
        state["undertone"] = "Warm"
    state["execution_status"] = "Skin tone color space analyzed."
    return state

def brand_catalog_stylist_node(state: AgentState) -> AgentState:
    """Agent node that utilizes LangChain tool-binding to invoke brand & accessory search tools."""
    llm = config.get_next_groq_client(temperature=0.7)
    llm_with_tools = llm.bind_tools(tools)
    
    brand = state.get('brand', 'Khaadi')
    pattern = state.get('pattern_choice', 'Floral')
    style = state.get('outfit_style', 'Co-ord Sets')
    skin = state.get('skin_tone', 'Medium')
    
    # Execute tools programmatically or let LLM trigger them
    direct_link = search_brand_catalog.invoke({
        "brand_name": brand,
        "pattern_keyword": pattern,
        "outfit_style": style
    })
    state['exact_filtered_link'] = direct_link
    state['tool_execution_logs'].append(f"Tool executed: search_brand_catalog for {brand}")
    
    footwear_data = fetch_footwear_accessories_links.invoke({"skin_tone": skin})
    state['tool_execution_logs'].append("Tool executed: fetch_footwear_accessories_links")
    
    prompt = f"""
    You are an elite Pakistani Fashion Designer and Personal Stylist.
    
    User Profile:
    - Gender: {state['gender']}
    - Height: {state['height']}
    - Body Shape: {state['body_shape']}
    - Target Brand: {brand}
    - Outfit Style: {style}
    - Selected Print/Pattern: {pattern}
    - Skin Tone: {skin} ({state['undertone']})
    - Budget Range: {state.get('budget')}
    
    Tool Output Data (Use these exact links in your response):
    - Direct Collection Search Link: [{brand} Collection]({direct_link})
    - Stylo Footwear Link: [Browse Matching Footwear on Stylo]({footwear_data['stylo_footwear']})
    - Borjan Khussa Link: [Browse Khussas on Borjan]({footwear_data['borjan_khussa']})
    
    Task Requirements:
    1. **Direct Filtered Product Search Link:** Embed the brand collection link above.
    2. **Body Architecture & Height Compatibility Verdict:** State "✅ SUITABLE" or "⚠️ NOT IDEAL" with fashion reasoning for {state['body_shape']} and {state['height']}.
    3. **3 Outfit Recommendations (Within {state.get('budget')}):** Detail outfit concept, fabric type, and price estimate.
    4. **Direct Shopping Links for Shoes & Accessories:** Embed the Stylo and Borjan links, plus metadata for metal color and jewelry.
    """
    
    messages = [
        SystemMessage(content="You are a top Pakistani luxury fashion consultant operating with tool-augmented workflows."),
        HumanMessage(content=prompt)
    ]
    
    response = llm_with_tools.invoke(messages)
    state['generated_recommendation'] = response.content
    state['execution_status'] = "Tool-augmented brand styling completed."
    return state

def market_fabric_tailor_node(state: AgentState) -> AgentState:
    llm = config.get_next_groq_client(temperature=0.7)
    
    prompt = f"""
    You are a master Pakistani Tailor and Fashion Designer.
    
    The user bought unstitched fabric and wants custom styling advice:
    - Gender: {state['gender']}
    - Height: {state['height']}
    - Body Shape: {state['body_shape']}
    - Skin Tone: {state['skin_tone']} ({state['undertone']})
    - Desired Vibe: {state.get('desired_vibe')}
    
    Provide a detailed stitching & styling plan:
    1. **Neckline & Sleeve Design:** (e.g., Angrakha gala, V-neck with organza lace, Tulip sleeves)
    2. **Trouser / Bottom Cut:** (e.g., Straight cigarette pants, Tulip shalwar, Flared gharara)
    3. **Dupatta & Trimming Contrast:** Exact contrast lace, organza border, or tassel ideas.
    4. **Footwear & Accessories Match:** Exact khussa / heel color and jewelry pairing.
    5. **Final Look Concept Summary:** Describe the complete final stitched appearance.
    """
    
    messages = [
        SystemMessage(content="You are a master Pakistani boutique designer."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    state['generated_recommendation'] = response.content
    state['execution_status'] = "Market fabric custom blueprint completed."
    return state


# ==============================================================================
# 4. CONDITIONAL EDGES & GRAPH COMPILATION
# ==============================================================================
def route_fashion_workflow(state: AgentState) -> str:
    if state.get("mode") == "brand_catalog":
        return "brand_catalog_stylist_node"
    else:
        return "market_fabric_tailor_node"

def build_style_sync_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("router_node", router_node)
    workflow.add_node("skin_analyzer_node", skin_analyzer_node)
    workflow.add_node("brand_catalog_stylist_node", brand_catalog_stylist_node)
    workflow.add_node("market_fabric_tailor_node", market_fabric_tailor_node)
    
    workflow.set_entry_point("router_node")
    workflow.add_edge("router_node", "skin_analyzer_node")
    
    workflow.add_conditional_edges(
        "skin_analyzer_node",
        route_fashion_workflow,
        {
            "brand_catalog_stylist_node": "brand_catalog_stylist_node",
            "market_fabric_tailor_node": "market_fabric_tailor_node"
        }
    )
    
    workflow.add_edge("brand_catalog_stylist_node", END)
    workflow.add_edge("market_fabric_tailor_node", END)
    
    return workflow.compile()

compiled_graph = build_style_sync_graph()