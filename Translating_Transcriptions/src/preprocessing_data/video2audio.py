import os
from moviepy import VideoFileClip
from pydub import AudioSegment, silence


class VideoToAudioConverter:
    def __init__(self, output_format="wav", sample_rate=16000, channels=1):
        self.output_format = output_format
        self.sample_rate = sample_rate
        self.channels = channels

    def convert(self, video_path, output_path=None):
        """
        Converts the extracted audio to a format best suited for Whisper Turbo 
        (wav format, 16 kHz, mono channel).
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # Ensure the output directory exists
        if output_path is None:
            output_path = f"{base_name}.{self.output_format}"
        else:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # If output_path is a directory, create a file in that directory
            if os.path.isdir(output_path):
                output_path = os.path.join(output_path, f"{base_name}.{self.output_format}")

        print(f"Extracting audio from {video_path}...")
        video_clip = VideoFileClip(video_path)
        audio_path = f"{base_name}_temp_audio.mp3"
        video_clip.audio.write_audiofile(audio_path, logger=None)
        video_clip.close()

        print(f"Converting audio to {self.output_format} with {self.sample_rate} Hz...")
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(self.sample_rate).set_channels(self.channels)
        audio.export(output_path, format=self.output_format)

        os.remove(audio_path)

        print(f"Audio saved to {output_path}")
        return output_path

    def split_audio(self, audio_path, output_path, segment_duration=15 * 60 * 1000, min_chunk_duration=12 * 60 * 1000,
                silence_threshold=-40, silence_chunk_length=1000):
        """
        Splits audio into segments of max `segment_duration` milliseconds, ensuring each chunk is at least 
        `min_chunk_duration` milliseconds. Splits are aligned to silence to preserve pronunciation.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Loading audio from {audio_path}...")
        audio = AudioSegment.from_file(audio_path)

        segments = []
        current_position = 0

        while current_position < len(audio):
            # Start with a segment of maximum duration
            chunk_end = min(current_position + segment_duration, len(audio))
            chunk = audio[current_position:chunk_end]

            # Ensure the chunk is at least `min_chunk_duration`
            if len(chunk) < min_chunk_duration and chunk_end < len(audio):
                extra_needed = min_chunk_duration - len(chunk)
                chunk = audio[current_position:chunk_end + extra_needed]
                chunk_end = current_position + len(chunk)

            # Adjust the end of the chunk to align with silence
            silence_ranges = silence.detect_silence(
                chunk,
                min_silence_len=silence_chunk_length,
                silence_thresh=silence_threshold
            )

            if silence_ranges:
                # Use the last silence range to align the cut, but only if chunk length >= min_chunk_duration
                _, cut_point = silence_ranges[-1]
                if cut_point >= min_chunk_duration:
                    chunk = chunk[:cut_point]

            segments.append(chunk)
            current_position += len(chunk)

        # Export segments
        segment_paths = []
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        for i, segment in enumerate(segments):
            segment_path = os.path.join(output_path, f"{base_name}_segment_{i + 1}.{self.output_format}")
            segment.export(segment_path, format=self.output_format)
            segment_paths.append(segment_path)
            print(f"Saved segment {i + 1} to {segment_path}")
        
        os.remove(audio_path)

        return segment_paths



if __name__ == "__main__":
    # Example usage
    converter = VideoToAudioConverter()
    # Step 1: Convert video to audio
    subject = "NLP"
    lecture_number = 2

    output_path = os.path.join("Lectures", subject, f"lecture{lecture_number}", "audio")
    input_path = os.path.join("Lectures", subject, f"lecture{lecture_number}", "video", "video.mp4")

    audio_path = converter.convert(video_path=input_path, output_path=output_path)
    # Step 2: Split the audio into segments
    segments = converter.split_audio(audio_path, output_path)
    print("Audio segments created:", segments)

