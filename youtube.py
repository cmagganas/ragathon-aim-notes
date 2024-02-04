import yt_dlp
import whisper

def download_mp4_from_youtube(url, filename):
    # Set the options for the download
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': filename,
        'quiet': True,
    }

    # Download the video file
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)

def transcribe_audio_from_youtube(url, filename):
    # Set the options for the download
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)

    for format in info["formats"][::-1]:
        if format["resolution"] == "audio only" and format["ext"] == "m4a":
            url = format["url"]
            break
            
    print(url)

    model = whisper.load_model("base")
    simulated_meeting_transcription = model.transcribe(url)
    with open(filename, "w") as file:
        file.write(simulated_meeting_transcription['text'])
    return simulated_meeting_transcription['text']


# Example usage
if __name__ == "__main__":

    simulated_meeting= "https://www.youtube.com/watch?v=i8KnCFq4Sw0"

    # Download the video file
    # download_mp4_from_youtube(simulated_meeting,"simulated_meeting.mp4")
    # model = whisper.load_model("base")
    # simulated_meeting_result = model.transcribe("simulated_meeting.mp4")
    # print(simulated_meeting_result['text'])

    # Transcribe the audio from url without downloading the video ... SLOW!
    print(transcribe_audio_from_youtube(simulated_meeting, "samples/simulated_meeting_transcription.txt"))


