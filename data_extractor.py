import os
import json
import litellm
from crewai import Agent, Task, Crew, LLM
litellm.register_model({
    "gpt-oss-20b": {  # <-- Ensure this perfectly matches the 'model=' string below
        "max_tokens": 128000,       # Set to the model's actual max context window
        "max_input_tokens": 128000, 
        "max_output_tokens": 9999,
        "litellm_provider": "openai", # Keep this as openai if it uses OpenAI-compatible endpoints
        "mode": "chat"
    }
})
def get_extractor_llm():
    """Uses the exact same LLM configuration as agents.py"""
    return LLM(
        model="nvidia_nim/meta/llama-3.3-70b-instruct",
        api_key=os.getenv("NVIDIA_API_KEY", ""),
        base_url="https://integrate.api.nvidia.com/v1",
        temperature=0.1, # Low temperature for strict JSON formatting
        max_tokens=8192, # Safe limit to avoid 400 Bad Request errors
    )

def extract_chart_data_to_json(results: dict, inputs: dict) -> dict:
    """
    Post-processing CrewAI Agent to parse raw text into strict JSON for the HTML graphs.
    """
    context = f"""
    SPONSOR OUTPUT:
    {results.get('sponsor_output', '')[:6500]}
    
    EXHIBITOR OUTPUT:
    {results.get('exhibitor_output', '')[:6500]}
    
    SPEAKER OUTPUT:
    {results.get('speaker_output', '')[:6500]}
    
    OPS OUTPUT (Risks):
    {results.get('ops_output', '')[:4500]}
    
    GTM OUTPUT (Channels):
    {results.get('gtm_output', '')[:6500]}
    
    DECISION LAYER OUTPUT:
    {results.get('decision_output', '')[:4500]}
    
    OUTREACH OUTPUT (Emails):
    {results.get('outreach_output', '')[:4500]}
    
    TOTAL BUDGET: {inputs.get('budget_range', '10000000')}
    """

    # 1. Define the Extractor Agent
    extractor_agent = Agent(
        role="JSON Data Extraction Specialist",
        goal="Extract quantitative data from text reports and convert them strictly into a valid JSON object.",
        backstory=(
            "You are a robotic data parser. You have no personality. "
            "Your ONLY output is raw, perfectly formatted JSON. "
            "You never output markdown formatting, conversational text, or explanations."
        ),
        llm=get_extractor_llm(),
        verbose=False,
        allow_delegation=False
    )

    # 2. Define the Extraction Task
    extraction_task = Task(
        description=f"""
        Read the following context and extract the quantitative data into a perfect JSON object.
        Normalize all Indian Rupee amounts into raw integers (e.g., "Rs. 40L" -> 4000000).
        Normalize all percentages into raw integers (e.g., "45%" -> 45).
        
        CONTEXT TO PARSE:
        {context}
        
        You MUST output ONLY valid JSON using this exact schema containing all 7 arrays:
        {{
          "sponsors": [
            {{"name": "Company X", "tier": 1, "relevance": 85, "feasibility": 90, "impact": 80, "composite": 125}}
          ],
          "exhibitors": [
            {{"cluster": "Startup", "booths": 10, "fee": 50000, "revenue": 500000}}
          ],
          "speakers": [
            {{"name": "Speaker Y", "archetype": "Academic", "influence": 88}}
          ],
          "risks": [
            {{"risk": "Speaker Cancellation", "prob": 45, "impact": 80}}
          ],
          "channels": [
            {{"channel": "React India Discord", "platform": "Discord", "reach": 5000, "score": 90, "cpr": 0}}
          ],
          "decisions": [
            {{"title": "Venue Selection", "confidence": 85, "decision": "Book the Marriott at 3.2L/day"}}
          ],
          "emails": [
            {{"label": "SPONSOR EMAIL 1", "type": "sponsor", "subject": "Exclusive Partnership", "to": "CMO, Company X", "body": "Email body content...", "cta": "Let's connect this Friday."}}
          ]
        }}
        
        Extract the top 5-8 items for each category. Do NOT wrap the output in ```json blocks. Just output the raw JSON string starting with {{.
        """,
        expected_output="A raw, valid JSON object starting with { and ending with }.",
        agent=extractor_agent
    )

    # 3. Create the Micro-Crew
    extraction_crew = Crew(
        agents=[extractor_agent],
        tasks=[extraction_task],
        verbose=False
    )

    try:
        print("  🧩 Post-processing: Extracting JSON data using CrewAI Extractor Agent...")
        
        # Kickoff the agent
        response_text = str(extraction_crew.kickoff()).strip()
        
        # Clean up in case the LLM wrapped it in markdown despite instructions
        if response_text.startswith("```json"):
            response_text = response_text.strip("`").replace("json\n", "", 1)
        elif response_text.startswith("```"):
            response_text = response_text.strip("`").strip()
            
        clean_data = json.loads(response_text)
        print("  ✅ JSON data successfully extracted!")
        return clean_data
        
    except json.JSONDecodeError as e:
        print(f"  ⚠️ JSON Decoding failed. The LLM output was not valid JSON: {e}")
        return {"sponsors": [], "exhibitors": [], "speakers": [], "risks": [], "channels": [], "decisions": [], "emails": []}
    except Exception as e:
        print(f"  ⚠️ Data extraction agent failed: {e}")
        return {"sponsors": [], "exhibitors": [], "speakers": [], "risks": [], "channels": [], "decisions": [], "emails": []}