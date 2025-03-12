import streamlit as st
import os
import asyncio
from video_processing import process_video, create_summary_video
from transcript_analysis import shorten_transcript

def main():
    st.title("Video Shortening App")
    
    uploaded_file = st.file_uploader("Upload a video (20 minutes or more)", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        # Save the uploaded video to a temporary file
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            transcript, timestamps = process_video("temp_video.mp4")
            st.success("Video uploaded successfully! Processing...")
            
            important_timestamps = asyncio.run(shorten_transcript(transcript, timestamps))
            
            summary_video_path = create_summary_video("temp_video.mp4", important_timestamps)
            st.video(summary_video_path)
        
        except ValueError as e:
            st.error(str(e))
        finally:
            if os.path.exists("temp_video.mp4"):
                try:
                    os.remove("temp_video.mp4")
                except PermissionError:
                    st.warning("Could not delete temp_video.mp4. Please close any applications using the file and try again.")

if __name__ == "__main__":
    main()