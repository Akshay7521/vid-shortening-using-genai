from typing import TypedDict, List

class Video(TypedDict):
    title: str
    duration: float  # Duration in seconds
    file_path: str

class Transcript(TypedDict):
    text: str
    timestamps: List[float]  # List of timestamps for each segment of the transcript