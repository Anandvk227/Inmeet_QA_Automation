import subprocess
import os

class ScreenRecorder:
    def __init__(self, output_path="Recordings", filename="test_recording.mp4"):
        self.output_path = output_path
        self.filename = filename
        self.process = None

    def start_recording(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        output_file = os.path.join(self.output_path, self.filename)
        command = [
            'ffmpeg',
            '-y',  # overwrite output file if it exists
            '-f', 'x11grab',  # grab the X11 display
            '-s', '1920x1080',  # screen resolution
            '-i', ':0.0',  # display number
            '-r', '25',  # frames per second
            output_file
        ]
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop_recording(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
