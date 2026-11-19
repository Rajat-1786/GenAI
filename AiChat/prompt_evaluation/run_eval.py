import asyncio
import json
import sys
from pathlib import Path
from anthropic import AsyncAnthropic

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from execute_query import execute_query
from model import JobDescriptionResponse

executor = execute_query(client=AsyncAnthropic())

#Code Grade
def grade(case, output):
    if case.get("expected_error", False):
        return {'valid': int(output is None)}
    if output is None:
        return {'valid': 0, 'title': 0, 'skills': 0, 'years_of_experience': 0}
    got = [x.lower() for x in output.skills]
    want = [x.lower() for x in case["skills"]]
    found = sum(any(w in g or g in w for g in got) for w in want)
    return {
        'valid':1,
        'title': 1 if output.title == case["title"] else 0,
        'skills': found / len(want) if want else 1,
        'years_of_experience': 1 if output.years_of_experience == case["years_of_experience"] else 0
    }

async def run_test_case(job_description):
    system_prompt = """You are a helpful assistant. Extract the title, skills and Years of Experience from the following job description and return only JSON with keys title, skills, years_of_experience" \
        Rule:
        1.  Treat No specific experience requirement as null for years_of_experience.
        2.  if Years of experience is in range then fetch the lowest value 
        3.  if job Description seems incorrect return the empty list of skills
    """
    try:
        result = await executor.get_json_response(job_description, system_prompt=system_prompt, temperature=0.0)
        return JobDescriptionResponse(**json.loads(result))
    except Exception as e:
        print(f"Error occurred while processing job description: {e}")
        return None


async def run_eval(dataset):
    final_output = []
    i = 0
    for entry in dataset:
        print(f"{i}: processing entry: {entry['description'][:50]}...")  # Print the first 50 characters of the description for context
        result = await run_test_case(entry["description"])
        # Need to compare the result with the expected output in the dataset entry
        final_output.append(grade(entry, result))
        i += 1
    print(f"Processed Successfully {len(final_output)}:")
    return final_output

async def main():
    with open("dataset.json", "r") as f:
        dataset = json.load(f)

    result = await run_eval(dataset)

    with open("eval_results.json", "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
