# AI Story Generator 📚✨

Generate full-length novels with AI! Harness the power of large language models to create engaging stories based on your prompts.

[![Discord](https://img.shields.io/discord/1255847829763784754?color=7289DA&label=Discord&logo=discord&logoColor=white)](https://discord.gg/R2SySWDr2s)

## 🚀 Features

- Generate medium to full-length novels: Produce substantial stories with coherent narratives, suitable for novella or novel-length works.
- Easy setup and use: Get started quickly with minimal configuration required.
- Customizable prompts and models: Choose from existing prompts or create your own, and select from various language models.
- Automatic model downloading: The system can automatically download required models via Ollama if they aren't already available.
- Support for local models via Ollama: Run language models locally for full control and privacy.
- Cloud provider support (currently Google): Access high-performance computing resources for those without powerful GPUs.
- Flexible configuration options: Fine-tune the generation process through easily modifiable settings.
- Works across all operating systems
- Supoorts translation of the generated stories in all languages

## 🏁 Quick Start

Getting started with AI Story Generator is easy:

1. Clone the repository
2. Install [Ollama](https://ollama.com/) for local model support
3. Run the generator:

```sh
./Write.py -Prompt Prompts/YourChosenPrompt.txt
```

That's it! The system will automatically download any required models and start generating your story.

**Optional steps:**

- Modify prompts in `Writer/Prompts.py` or create your own
- Configure the model selection in `Writer/config.py`

## 💻 Hardware Recommendations

Not sure which models to use with your GPU? Check out our [Model Recommendations](Docs/Models.md) page for suggestions based on different GPU capabilities. We provide a quick reference table to help you choose the right models for your hardware, ensuring optimal performance and quality for your story generation projects.

## 🛠️ Usage

You can customize the models used for different parts of the story generation process in two ways:

### 1. Using Writer/Config.py

Edit the `Writer/Config.py` file to change the default models:

```python
INITIAL_OUTLINE_WRITER_MODEL = "ollama://llama3:70b"
CHAPTER_OUTLINE_WRITER_MODEL = "ollama://gemma2:27b"
CHAPTER_WRITER_MODEL = "google://gemini-1.5-flash"
...
```

### 2. Using Command-Line Arguments

You can override the default models by specifying them as command-line arguments:

```sh
./Write.py -Prompt Prompts/YourChosenPrompt.txt -InitialOutlineModel "ollama://llama3:70b" ...
```

Available command-line arguments are stated in the `Write.py` file.

The model format is: `{ModelProvider}://{ModelName}@{ModelHost}`

- Default host is `127.0.0.1:11434` (currently only affects ollama)
- Default ModelProvider is `ollama`
- Supported providers: `ollama`, `google`, `openrouter`

Example:
```sh
./Write.py -Prompt Prompts/YourChosenPrompt.txt -InitialOutlineModel "google://gemini-1.5-pro" -ChapterOutlineModel "ollama://llama3:70b@192.168.1.100:11434"
```

This flexibility allows you to experiment with different models for various parts of the story generation process, helping you find the optimal combination for your needs.

## 🧰 Architecture Overview

![Block Diagram](Docs/BlockDiagram.drawio.svg)

## 🛠️ Customization

- Experiment with different local models via Ollama: Try out various language models to find the best fit for your storytelling needs.
- Test various model combinations for different story components: Mix and match models for outline generation, chapter writing, and revisions to optimize output quality.

## 💪 What's Working Well

- Generating decent-length stories: The system consistently produces narratives of substantial length, suitable for novella or novel-length works.
- Character consistency: AI models maintain coherent character traits and development throughout the generated stories.
- Interesting story outlines: The initial outline generation creates compelling story structures that serve as strong foundations for the full narratives.

## 🔧 Areas for Improvement

- Reducing repetitive phrases: We're working on enhancing the language variety to create more natural-sounding prose.
- Improving chapter flow and connections: Efforts are ongoing to create smoother transitions between chapters and maintain narrative cohesion.
- Addressing pacing issues: Refinements are being made to ensure proper story pacing and focus on crucial plot points.
- Optimizing generation speed: We're continuously working on improving performance to reduce generation times without sacrificing quality.

## 🤝 Contributing

We're excited to hear from you! Your feedback and contributions are crucial to improving the AI Story Generator. Here's how you can get involved:

1. 🐛 **Open Issues**: Encountered a bug or have a feature request? [Open an issue](https://github.com/datacrystals/AIStoryWriter/issues) and let us know!

2. 💡 **Start Discussions**: Have ideas or want to brainstorm? [Start a discussion](https://github.com/datacrystals/AIStoryWriter/discussions) in our GitHub Discussions forum.

3. 🔬 **Experiment and Share**: Try different model combinations and share your results. Your experiments can help improve the system for everyone!

4. 🖊️ **Submit Pull Requests**: Ready to contribute code? We welcome pull requests for improvements and new features.

5. 💬 **Join our Discord**: For real-time chat, support, and community engagement, [join our Discord server](https://discord.gg/R2SySWDr2s).

Don't hesitate to reach out – your input is valuable, and we're here to help!

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). This means that if you modify the code and use it to provide a service over a network, you must make your modified source code available to the users of that service. For more details, see the [LICENSE](LICENSE) file in the repository or visit [https://www.gnu.org/licenses/agpl-3.0.en.html](https://www.gnu.org/licenses/agpl-3.0.en.html).

---

Join us in shaping the future of AI-assisted storytelling! 🖋️🤖
