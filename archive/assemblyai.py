import os
import yt_dlp
import archive.assemblyai as aai
from dotenv import load_dotenv

def transcribe_youtube_video(youtube_link, output_to_file=False):
    """
    Extracts audio from a YouTube video, transcribes it using AssemblyAI,
    and optionally outputs the transcript to a text file.

    Parameters:
    - youtube_link (str): The YouTube video URL to transcribe.
    - output_to_file (bool): If True, saves the transcript to a file and returns its path.
                             If False, returns the transcript text directly.

    Returns:
    - str: The path to the transcript file or the transcript text, depending on output_to_file flag.
    """
    # Extract audio URL from YouTube link
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(youtube_link, download=False)
        audio_url = next((format["url"] for format in info["formats"][::-1]
                          if format["resolution"] == "audio only" and format["ext"] == "m4a"), None)
        if not audio_url:
            raise ValueError("Audio URL could not be found.")

    # Configure AssemblyAI
    load_dotenv()

    aai.settings.api_key = f"{os.environ['ASSEMBLYAI_API_KEY']}"
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(audio_url, config)

    # Output handling
    if output_to_file:
        filename = 'transcript-with-diarization-sample.txt'
        with open(filename, 'w') as f:
            for utterance in transcript.utterances:
                f.write(f"Speaker {utterance.speaker}: {utterance.text}\n")
        return os.path.abspath(filename)
    else:
        return '\n'.join(f"Speaker {utterance.speaker}: {utterance.text}" for utterance in transcript.utterances)

if __name__ == "__main__":
    # Example usage
    youtube_link = 'https://www.youtube.com/watch?v=i8KnCFq4Sw0'
    # To get transcript text directly
    transcript_text = transcribe_youtube_video(youtube_link, output_to_file=False)
    print(transcript_text)
    # To save transcript to a file and get the file path
    transcript_file_path = transcribe_youtube_video(youtube_link, output_to_file=True)
    print(f"Transcript saved to: {transcript_file_path}")
