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

simulated_meeting= "https://www.youtube.com/watch?v=i8KnCFq4Sw0"
download_mp4_from_youtube(simulated_meeting,"simulated_meeting.mp4")
model = whisper.load_model("base")
simulated_meeting_result = model.transcribe("simulated_meeting.mp4")
print(simulated_meeting_result['text'])


