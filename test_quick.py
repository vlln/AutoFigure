"""
AutoFigure 测试脚本 - 使用 deepseek-v4-pro (文本) + qwen-vl-max (评估)
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

errors = config.validate()
if errors:
    print(f"  Config errors: {errors}")
    exit(1)

agent = AutoFigureAgent(config)

print(f"\n{'='*60}")
print(f"  Generating: CNN Architecture Diagram")
print(f"{'='*60}\n")

result = agent.generate(
    description="A CNN model architecture for image classification, "
                "showing input layer, two convolutional layers with ReLU, "
                "pooling layers, and a fully connected output layer.",
    max_iterations=2,
    output_format="svg",
    topic="paper",
)

print(f"\n{'='*60}")
print(f"  Result")
print(f"{'='*60}")
if result.success:
    print(f"  Status:       SUCCESS")
    print(f"  SVG:          {result.svg_path}")
    print(f"  Preview:      {result.preview_path}")
    print(f"  Final score:  {result.final_score}/10")
    print(f"  Iterations:   {result.iterations_used}")
else:
    print(f"  Status: FAILED")
    print(f"  Error:  {result.error}")

print(f"\n  Logs:")
for log in result.logs:
    print(f"    - {log}")