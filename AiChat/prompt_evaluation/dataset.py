import asyncio
import json
import sys
from pathlib import Path

# Make the parent AiChat directory importable (execute_query, config live there)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from anthropic import AsyncAnthropic
from execute_query import execute_query

async def generate_dataset():
    prompt = """
        Generate an evaluation dataset for a job-description extraction task.
        Return a JSON array of 25 objects. out of 25 20 object has:
        - "description": a realistic job posting, 3 to 8 sentences
        - "title": the job title exactly as the description states it
        - "skills": the technical skills named in the description (list of strings)
        - "years_of_experience": integer, or null if the description gives no years

         and  5 object have harder cases: missing years (null), missing skills ([]), a long messy posting, a different year format (“five years”), and one non-job text in the description.


        Rules:
        - Every skill and the title must appear in the description text.
        - Vary style, length and seniority (startup, enterprise, junior, senior, informal, formal).
        - Include these edge cases: 2 with no years stated, 1 with a range like "3-5 years" (use the lower number),
        1 with skills only mentioned inside sentences, 1 with a very short description.
        - Do not repeat job titles.

        Example output:
        ```json
        [
        {
            "description": "We are hiring a Backend Engineer with 4+ years of experience in Python and FastAPI...",
            "title": "Backend Engineer",
            "skills": ["Python", "FastAPI"],
            "years_of_experience": 4
        }
        ]
        ```

        Return only the JSON array.
        """

    executor = execute_query(client=AsyncAnthropic())

    result = await executor.get_json_response(prompt, temperature=0.7)
    dataset = json.loads(result)
    print(f"Generated dataset with {len(dataset)} entries.")
    with open("dataset.json","w") as f:
        json.dump(dataset, f, indent=2)

if __name__ == "__main__":
    asyncio.run(generate_dataset())
