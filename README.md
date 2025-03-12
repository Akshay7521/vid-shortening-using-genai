# vid-shortening-using-genai

## Overview

This application allows users to upload long videos (20 minutes or more) and generates a shortened version by identifying and extracting the most important segments. The app uses Azure OpenAI for transcript analysis and video processing libraries to create the summary video.

## Features

- Upload videos in various formats (mp4, mov, avi).
- Automatically transcribes the video and analyzes the transcript.
- Generates a summary video containing only the important segments.
- Displays the summary video within the app.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/vid-shortening-using-genai.git
    cd vid-shortening-using-genai
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root directory and add the following variables:

    ```env
    ENDPOINT_URL=your_azure_openai_endpoint_url
    DEPLOYMENT_NAME=your_azure_openai_deployment_name
    AZURE_OPENAI_API_KEY=your_azure_openai_api_key
    AZURE_OPENAI_VERSION=your_azure_openai_version
    ```

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Upload a video file (20 minutes or more) using the file uploader.

4. Wait for the video to be processed. The app will display the summary video once processing is complete.

## File Structure

- `app.py`: The main Streamlit application file.
- `index.py`: Contains type definitions for video and transcript data.
- `transcript_analysis.py`: Handles transcript analysis using Azure OpenAI.
- `video_shortening.py`: Contains functions for video processing and summary creation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Azure OpenAI](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/)
- [MoviePy](https://zulko.github.io/moviepy/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pydub](https://pydub.com/)