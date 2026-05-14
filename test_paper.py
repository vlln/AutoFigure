"""
AutoFigure 测试 - 从 PDF 论文提取方法论并生成配图
"""
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

from autofigure import AutoFigureAgent, Config

config = Config.from_env()

print("=" * 60)
print("  Model Configuration")
print("=" * 60)
print(f"  Text (generate/improve): {config.generation_model}")
print(f"  Vision (evaluate):       {config.evaluation_model}")
print(f"  Image (enhancement):     {config.enhancement_model}")
print(f"  Base URL:                {config.generation_base_url}")
print(f"  Methodology model:       {config.methodology_model}")

errors = config.validate()
if errors:
    print(f"  Config errors: {errors}")
    exit(1)

agent = AutoFigureAgent(config)

paper_path = os.path.expanduser(
    "~/agent-space/repro-test/008/repro-data/01_plan/resources/paper.pdf"
)

print(f"\n{'='*60}")
print(f"  Paper: {paper_path}")
print(f"{'='*60}\n")

result = agent.generate_from_paper(
    paper_path=paper_path,
    max_iterations=3,
    output_format="svg",
)

print(f"\n{'='*60}")
print(f"  Result")
print(f"{'='*60}")
if result.success:
    print(f"  Status:           SUCCESS")
    print(f"  SVG:              {result.svg_path}")
    print(f"  Preview:          {result.preview_path}")
    print(f"  Final score:      {result.final_score}/10")
    print(f"  Iterations:       {result.iterations_used}")
    if result.methodology_text:
        print(f"  Methodology:      {len(result.methodology_text)} chars")
else:
    print(f"  Status: FAILED")
    print(f"  Error:  {result.error}")

print(f"\n  Logs:")
for log in result.logs:
    print(f"    - {log}")

if result.methodology_text:
    print(f"\n{'='*60}")
    print(f"  Extracted Methodology (first 2000 chars)")
    print(f"{'='*60}")
    print(result.methodology_text[:2000])