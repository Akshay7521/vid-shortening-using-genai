import cv2
import moviepy as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def check_video_duration(video_path):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps / 60  # duration in minutes
    video.release()

    return duration

def transcribe_audio_with_timestamps(audio_path):
    # Load the audio file
    audio = AudioSegment.from_file(audio_path)
    
    # Split audio where silence is 1500ms or more and get chunks
    chunks = split_on_silence(audio, min_silence_len=1800, silence_thresh=-40)
    
    recognizer = sr.Recognizer()
    timestamps = []
    current_time = 0
    
    for i, chunk in enumerate(chunks):
        chunk_silent = AudioSegment.silent(duration=10)
        audio_chunk = chunk_silent + chunk + chunk_silent
        chunk_filename = f"chunk{i}.wav"
        audio_chunk.export(chunk_filename, format="wav")
        
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_listened)
                start_time = current_time
                end_time = current_time + len(chunk) / 1000.0
                timestamps.append((start_time, end_time, text))
                print(f"Chunk {i}: {start_time}-{end_time}: {text}")
            except sr.UnknownValueError:
                timestamps.append((current_time, current_time + len(chunk) / 1000.0, "[Unintelligible]"))
            except sr.RequestError as e:
                timestamps.append((current_time, current_time + len(chunk) / 1000.0, f"[Error: {e}]"))
        
        current_time += len(chunk) / 1000.0  # Update current time in seconds
    
    return timestamps

def extract_transcript(video_path):
    audio_file = video_path.replace('.mp4', '.wav')

    # Convert video to audio
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_file)
    video.close()  # Ensure the video file is closed

    # Transcribe audio with timestamps
    timestamps = transcribe_audio_with_timestamps(audio_file)
    transcript = " ".join([text for _, _, text in timestamps])
    
    return transcript, timestamps

def process_video(video_path):
    duration = check_video_duration(video_path)
    if duration < 20:
        raise ValueError("Video must be at least 20 minutes long.")
    
    transcript, timestamps = extract_transcript(video_path)
    return transcript, timestamps

def create_summary_video(video_path, important_timestamps):
    video = mp.VideoFileClip(video_path)
    clips = [video.subclipped(ts['start'], ts['end']) for ts in important_timestamps]
    summary_video = mp.concatenate_videoclips(clips)
    summary_video_path = "summary_video.mp4"
    summary_video.write_videofile(summary_video_path)
    video.close()  # Ensure the video file is closed
    return summary_video_path