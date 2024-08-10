import os
import openai
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


def get_transcript(youtube_url):
    try:
        video_id = youtube_url.split("v=")[-1]
        # Fetch the transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Convert the transcript list to a plain text format
        formatter = TextFormatter()
        transcript = formatter.format_transcript(transcript_list)
        print(transcript)

        return transcript
    except NoTranscriptFound:
        print(f"No transcript found for the video: {youtube_url}")
        return None
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for the video: {youtube_url}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def summarize_transcript(transcript):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following transcript and give me the main points in bullet points:\n\n{
                    transcript}"}
            ],
            temperature=0.5
        )

        summary = response.choices[0].message.content

        return summary
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while summarizing: {e}")
        return None


def main(youtube_url):
    transcript = get_transcript(youtube_url)

    if transcript is None:
        print("Could not retrieve transcript.")
    else:
        print("Transcript retrieved successfully.")
        summary = summarize_transcript(transcript)

        if summary is None:
            print("Could not generate summary.")
        else:
            print("\nSummary of the video:\n")
            print(summary)


if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ")
    main(youtube_url)
