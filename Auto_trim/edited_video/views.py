from django.http import JsonResponse,FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
import os
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import VideoFileClip, concatenate_videoclips

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        id = request.POST.get('id')
      
        file = request.FILES.get('file')  # Handle the uploaded file

        if file:
            custom_path = os.path.join('upload', file.name)
            file_name = default_storage.save(custom_path, file)
            getfile(f"{os.path.join( file_name )}" ,id)
           

        return JsonResponse({'message': 'Data received successfully!', 'id': id,})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def download_video(request, file_name):
 if request.method == 'GET':   
    # Path to the directory where your video files are stored
    video_path = os.path.join('Data', file_name)
    
    # Check if the file exists
    if os.path.exists(video_path):
        # Send the video file as an attachment (download)
        response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'  # 'attachment' forces download
        return response
    else:
        raise Http404("Video not found.")


def trim(video_id):
    # Get the list of available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    # Fetch the transcript in Hindi (language code 'hi')
    try:
        transcript = transcript_list.find_transcript(['hi'])
        hindi_transcript = transcript.fetch()
        
        final_list = []
        is_cutting = False
        start_time = 0

        # Iterate through the transcript
        for item in hindi_transcript:
            # Check for the "Start cutting" cue
            if item['text'].lower() == "start triming":  # Using .lower() for case-insensitive match
                is_cutting = True
                start_time = item['start'] - 1  # Adjust start time as needed
                
            # Check for the "end cutting" cue
            elif item['text'].lower() == "end triming" and is_cutting:
                end_time = item['start'] + 1  # Adjust end time as needed
                final_list.append((start_time, end_time))
                is_cutting = False  # Reset for the next potential segment

        # Return the final list of start and end times
        return final_list

    except Exception as e:
        print(f"Error: {e}")
        return []





def getfile(path, id):
    # Get the list of segment times to cut out (start and end times)
    lists = trim(id)
    
    # Load the video file from the given path
    video = VideoFileClip(path)

    # Create a list to store the video segments that are kept
    segments = []
    
    # Initialize start of the video
    current_start = 0

    # Loop through the segment times and extract the parts before each segment
    for start_time, end_time in lists:
        # Extract the part before the current segment to cut out
        if current_start < start_time:
            segment = video.subclip(current_start, start_time)
            segments.append(segment)
        
        # Update current start time to the end of the current cutout segment
        current_start = end_time

    # Add the remaining part of the video after the last segment
    if current_start < video.duration:
        last_segment = video.subclip(current_start, video.duration)
        segments.append(last_segment)

    # Concatenate all the kept segments into the final video
    final_video = concatenate_videoclips(segments)

    # Create the directory path if it doesn't exist
    custom_path = os.path.join('Data', id)
    os.makedirs(os.path.dirname(custom_path), exist_ok=True)

    # Save the final video to the specified path
    final_video.write_videofile(f"{custom_path}.mp4", codec="libx264")

    # Return the final video file path
    return f"{custom_path}.mp4"
