import cv2
import PySimpleGUI as sg
from pytube import YouTube
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, world!')

        # Load video file
        cap = cv2.VideoCapture('yt.mp4')

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create OpenCV window
        cv2.namedWindow('YT DOWNLOADER', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('YT DOWNLOADER', frame_width, frame_height)

        # Set timer for splash screen
        start_time = time.time()
        while (time.time() - start_time) < 4.5:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('YT DOWNLOADER', frame)
            cv2.waitKey(int(2000/fps))

        # Close OpenCV window and release video capture
        cv2.destroyAllWindows()
        cap.release()

        # Create main window
        sg.theme('Dark Amber')
        layout = [[sg.Text("Enter the URL of the YouTube video you want to download:")],
                  [sg.Input(key="-URL-")],
                  [sg.Button('Download')],
                  [sg.Text(key="-TITLE-")],
                  [sg.Text(key="-VIEWS-")],
                  [sg.Text(key="-CONFIRMATION-")]]

        window = sg.Window('YouTube Video Downloader', layout, icon='yt1.ico')

        # Create function to download video
        def download_video():
            # Get URL input from user
            url = values["-URL-"]

            # Create YouTube object
            yt = YouTube(url)

            # Print video details
            window["-TITLE-"].update("Title: " + yt.title)
            window["-VIEWS-"].update("Views: " + str(yt.views))

            # Ask user for download path
            download_folder = sg.popup_get_folder('Choose a download folder')

            # Create download directory if it doesn't exist
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            # Get highest resolution stream
            yd = yt.streams.get_highest_resolution()

            # Download video to specified path
            yd.download(download_folder)

            # Print confirmation message
            window["-CONFIRMATION-"].update("Video downloaded successfully to " + download_folder)

        # Event loop
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Download':
                download_video()

        window.close()


httpd = HTTPServer(('localhost', PORT), handler)
print(f'Starting server at http://localhost:{PORT}')
httpd.serve_forever()
