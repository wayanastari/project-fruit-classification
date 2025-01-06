// main.js
const useCameraButton = document.getElementById("useCamera");
const uploadImageButton = document.getElementById("uploadImage");
const predictButton = document.getElementById("predict");
const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const predictionResult = document.getElementById("predictionResult");

let imageTaken = false;

// Function to start camera
function startCamera() {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      const video = document.createElement("video");
      video.id = "cameraFeed";
      video.srcObject = stream;
      video.play();

      const captureButton = document.createElement("button");
      captureButton.textContent = "Capture";
      captureButton.id = "captureButton";

      document.body.appendChild(video);
      document.body.appendChild(captureButton);

      captureButton.addEventListener("click", () => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        preview.src = canvas.toDataURL("image/png");
        imageTaken = true;
        predictButton.disabled = false;

        stream.getTracks().forEach((track) => track.stop());
        video.remove();
        captureButton.remove();
      });
    })
    .catch((error) => {
      alert("Unable to access camera: " + error.message);
    });
}

// Event listeners
useCameraButton.addEventListener("click", startCamera);

uploadImageButton.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      preview.src = reader.result;
      imageTaken = true;
      predictButton.disabled = false;
    };
    reader.readAsDataURL(file);
  }
});

predictButton.addEventListener("click", async () => {
  if (!imageTaken) {
    alert("No image selected or captured!");
    return;
  }

  const formData = new FormData();
  const blob = await fetch(preview.src).then((res) => res.blob());
  formData.append("file", blob, "image.png");

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    predictionResult.textContent = `Prediction: Class ${
      result.class
    }, Confidence: ${(result.confidence * 100).toFixed(2)}%`;
  } catch (error) {
    predictionResult.textContent = `Error: ${error.message}`;
  }
});
