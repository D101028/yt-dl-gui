import ffmpeg
import os

def join_video_and_audio(vp: str, ap: str, output: str | None = None, to_remove: bool = False):
    """
    Joins a video file (vp) and an audio file (ap) into a single output file (output).
    
    Args:
    vp (str): Path to the video file.
    ap (str): Path to the audio file.
    output (str): Path where the output file will be saved. If None, saves as the same as vp (will remove original vp).
    """
    if output is None:
        temp = vp.split(".")
        output_filename = ".".join(temp[:-1]) + "_temp." + temp[-1]
    else:
        output_filename = output

    try:
        # Use ffmpeg to combine video and audio
        # Use ffmpeg to combine the video and audio
        video_input = ffmpeg.input(vp)
        audio_input = ffmpeg.input(ap)
        
        # Merge the video and audio inputs into the output file
        ffmpeg.output(video_input, audio_input, output_filename, vcodec='copy', acodec='aac').run(overwrite_output=True)
        if output is None:
            os.remove(vp)
            if to_remove:
                os.remove(ap)
            os.rename(output_filename, vp)
        else:
            if to_remove:
                os.remove(vp)
                os.remove(ap)
    except ffmpeg.Error as e:
        print("An error occurred while processing:")
        print(e.stderr)
