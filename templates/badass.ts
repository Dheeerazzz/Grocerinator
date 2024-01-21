    <script>
        // Get the video element
        const video = document.getElementById('cameraFeed');
    
        // Request access to the camera
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                video.srcObject = stream;
            })
            .catch((error) => {
                console.error('Error accessing camera:', error);
            });
    
        function performOCR() {
            // Create a canvas to draw the current frame
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
            // Convert canvas to base64 image
            const dataUrl = canvas.toDataURL('image/jpeg');
            const base64Image = dataUrl.split(',')[1];
    
            // Send the image to the server for OCR processing
            fetch('/process_ocr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: base64Image }),
            })
            .then(response => response.json())
            .then(result => {
                // Display the OCR result
                document.getElementById('ocrResult').textContent = result.result;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    </script>
    <div class="card-body">
                                        <center>
                                            <h5 class="card-title">Scan Results</h5>
                                            <video id="cameraFeed" width="640" height="480" autoplay></video><br>
                                            <button type="button" class="btn btn-secondary" onclick="performOCR()">Scan and Process</button>
                                            <div id="ocrResult"></div>
                                        </center>
                                    </div>