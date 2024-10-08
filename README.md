# PyGen

PyGen is a Python-based project designed to generate a random PDF extracted using wikipedia API, and then using Gemini API paraphrases the content This tool can be used for various things such as uploading to StuDocu or CourseHero.

## Installation

To install PyGen, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/PyGen.git
    ```
2. Navigate to the project directory:
    ```bash
    cd PyGen
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

To run this project, you need to configure your API key. You will need a Google account to get access to the Gemini API key.

1. Create a `.env` file in the root directory of the project.
2. Add the following line to the `.env` file:

`API_KEY=your_api_key_here`

Or you can set this as an environment variable.

## Usage

To use PyGen, run the following command:
```bash
python main.py num
```
Replace num with how many pdfs you want to generate.

## Contact

For any questions or suggestions, please open an issue or contact k499wang@uwaterloo.ca.
