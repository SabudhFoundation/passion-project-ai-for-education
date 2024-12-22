import whisper
import os
import pickle
from typing import List, Dict

class Transcriber:
    def __init__(self, model="turbo"):
        """
        Initialize the Transcriber with the specified Whisper model and SpaCy language model.
        
        :param model: Whisper model to use for transcription
        :param language: SpaCy language model for sentence boundary detection
        """
        print("Initializing the Whisper model...")
        self.model = whisper.load_model(model)
        print(f"Model '{model}' loaded successfully.")

    def transcribe(self, audio_path, topic, subject, verbose=False):
        """Transcribes the given audio file with context-specific prompts."""
        print(f"Starting transcription for file: {audio_path}")
        print(f"Topic: {topic}, Subject: {subject}")
        prompt = (
            f"Transcribe a lecture on the topic '{topic}' from the subject '{subject}'.Please transcribe clearly and accurately, focusing on key terms relevant to the topic."
        )
        
        try:
            # Perform transcription
            result = self.model.transcribe(
                    audio_path,
                    verbose=verbose,  # Keeps verbosity based on user input
                    temperature=(0.2, 0.3, 0.5, 0.7),  # Balances determinism and creativity
                    initial_prompt=prompt,  # Uses the provided prompt
                    compression_ratio_threshold=2.2,  # Default, good for filtering compressed outputs
                    logprob_threshold=-0.8,  # Default, filters very uncertain words
                    no_speech_threshold=0.5,  # Slightly lower to detect speech in low-volume audio
                    condition_on_previous_text=False,  # Maintains context for better results
                    word_timestamps=True,  # Includes word-level timestamps
                    prepend_punctuations="\"'“¿([{-",  # Default punctuation settings
                    append_punctuations="\"'.。,，!！?？:：”)]}、",  # Default punctuation settings
                    clip_timestamps="0",  # Default timestamp clipping
                                )

            print("Transcription completed successfully.")
            print(f"Total segments: {len(result['segments'])}")
        except Exception as e:
            print(f"Error during transcription: {e}")
            raise

        # Process and merge segments
        merged_segments = self._merge_segments(result["segments"])
        print(f"Merged into {len(merged_segments)} subtitle segments.")
        os.remove(audio_path)

        return merged_segments, result['text']

    def _merge_segments(self, segments: List[Dict[str, float]]) -> List[Dict[str, float]]:
        """
        Merges transcription segments to ensure each segment is between 10 and 20 seconds in duration.

        :param segments: List of segment dictionaries with 'text', 'start', and 'end' keys
        :return: List of merged segment dictionaries
        """
        print("Merging transcription segments...")
        merged = []
        current_text = ""
        segment_start_time = None

        for i, segment in enumerate(segments):
            print(f"Processing segment {i}: {segment['text']}")

            if segment_start_time is None:
                segment_start_time = segment['start']

            # Append current segment text
            current_text += (" " if current_text else "") + segment['text']

            # Calculate duration with the current segment
            current_duration = segment['end'] - segment_start_time

            # If duration exceeds 20 seconds or is the last segment, finalize the current batch
            if current_duration >= 20 or (i + 1 == len(segments)):
                merged.append({
                    'text': current_text.strip(),
                    'start': segment_start_time,
                    'end': segment['end']
                })
                print(f"Added merged segment: [{segment_start_time:.2f} - {segment['end']:.2f}] {current_text.strip()}")

                # Reset for the next batch
                current_text = ""
                segment_start_time = None

            # If the duration is below 10 seconds, keep merging until it meets the minimum threshold
            elif i + 1 < len(segments):
                next_duration = segments[i + 1]['end'] - segment_start_time
                if next_duration >= 10:
                    merged.append({
                        'text': current_text.strip(),
                        'start': segment_start_time,
                        'end': segment['end']
                    })
                    print(f"Added merged segment: [{segment_start_time:.2f} - {segment['end']:.2f}] {current_text.strip()}")

                    # Reset for the next batch
                    current_text = ""
                    segment_start_time = None

        # Handle any remaining text not merged
        if current_text:
            merged.append({
                'text': current_text.strip(),
                'start': segment_start_time,
                'end': segments[-1]['end']
            })
            print(f"Added final merged segment: [{segment_start_time:.2f} - {segments[-1]['end']:.2f}] {current_text.strip()}")

        print("Segment merging completed.")
        return merged

# Rest of the code remains the same as in the previous implementation
if __name__ == "__main__":
    subject = "NLP"
    lecture_number = 2
    transcription = ""
    parent_path = rf"Lectures\{subject}\lecture{lecture_number}"
    if os.path.exists(os.path.join(parent_path, "subtitles-obj.pkl")):
        with open(os.path.join(parent_path, "subtitles-obj.pkl"), "rb") as file:
            subtitles = pickle.load(file)
        for s in subtitles:
            transcription += s['text']
    else:
        audio_paths = [os.path.join(parent_path,"audio", wav) for wav in os.listdir(os.path.join(parent_path, "audio"))]
        
        print("Initializing the Transcriber class...")
        transcriber = Transcriber(model="turbo")

        subtitles = []
        # Check if file exists before transcription
        for audio_path in audio_paths:
            if not os.path.exists(audio_path):
                print(f"Error: Audio file not found at {audio_path}")
                exit(1)
        
            try:
                seg_subtitles, seg_transcription = transcriber.transcribe(
                    audio_path=audio_path,
                    topic="Vectorization",
                    subject="Natural Language Processing",
                    verbose=True
                )
                print("Subtitle generation completed.")
            except Exception as e:
                print(f"Error during subtitle generation: {e}")
                import traceback
                traceback.print_exc()
            if subtitles:
                last_time = subtitles[-1]['end']
                for subtitle in seg_subtitles:
                    subtitle['start'] += last_time
                    subtitle['end'] += last_time
            transcription += seg_transcription
            subtitles.extend(seg_subtitles)

        # Saving subtitles
        with open(os.path.join(parent_path,'subtitles-obj.pkl'), 'wb') as file:
            pickle.dump(subtitles, file)

        # Save subtitles to a .vtt file
        vtt_file_path = os.path.join(parent_path, "english-subtitles.vtt")
        with open(vtt_file_path, 'w', encoding='utf-8') as vtt_file:
            vtt_file.write("WEBVTT\n\n")  # Write header for WebVTT format
            for i, subtitle in enumerate(subtitles):
                # Convert start and end times to the required format (HH:MM:SS.MS)
                start_time = subtitle['start']
                end_time = subtitle['end']
                start_time_vtt = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{start_time % 60:06.3f}"
                end_time_vtt = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{end_time % 60:06.3f}"

                # Write the subtitle in WebVTT format
                vtt_file.write(f"{i+1}\n")  # Subtitle number
                vtt_file.write(f"{start_time_vtt} --> {end_time_vtt}\n")  # Time range
                vtt_file.write(f"{subtitle['text']}\n\n")  # Subtitle text
                print(f"Subtitles saved to {vtt_file_path}")
    
    # Save transcription
    with open(os.path.join(parent_path, "transcription_text.txt"), "w") as file:
        file.writelines(transcription)
        