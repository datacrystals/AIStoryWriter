# Model Recommendations for Different GPU Capabilities

Use this table as a guide to choose appropriate models based on your GPU's VRAM. These are general recommendations and may vary based on specific hardware configurations and other running processes.

| VRAM Capacity | Recommended Models              | Notes                                                                                                  |
| ------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 4-6 GB        | aya:7b, phi:3b, tinyllama:1.5b  | Suitable for very basic story generation. Strong limitations                                           |
| 8-12 GB       | llama3:8b, mistral:7b, phi:7b, gemma2:9b   | Good for general story generation tasks. Still lacking at some points but generats consistent stories. |
| 16-24 GB      | ?                               | Capable of generating more complex and coherent stories. Good for most users.                          |
| 32-48 GB      | llama3:70b                      | High-quality output with improved coherence and creativity. Recommended for advanced projects.         |
| 64+ GB        | miqulitz120b, midnight-miqu103b | Top-tier performance. Ideal for professional use and generating consistent novel-length content.       |
| Cloud         | google/gemini-1.5-flash         | Good quality and very cheap, good for most users.                                                      |
| Cloud         | google/gemini-1.5-pro           | Expensive but good for high-quality, professional use.                                                 |

## Notes:

- Adjust your choice based on the specific requirements of your project and the performance you observe.
- Experiment with different models to find the best balance between quality and generation speed for your setup.
- Remember to close other GPU-intensive applications when running larger models.
- For multi-GPU setups, you may be able to run larger models than indicated here.

Always check the latest Ollama documentation for the most up-to-date model availability and requirements.

## Feedback

If you have any feedback or suggestions on this guide, please feel free to reach out! We always appreciate hearing from our users.
