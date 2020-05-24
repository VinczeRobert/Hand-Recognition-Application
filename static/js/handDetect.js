const s = document.getElementById('handDetect');
const sourceVideo = s.getAttribute("data-source");
const uploadWidth = s.getAttribute("data-uploadWidth") || 640;
const mirror = s.getAttribute("data-mirror") || false;
const scoreThreshold = s.getAttribute("data-scoreThreshold") || 0.5;

v = document.getElementById(sourceVideo);

let isPlaying = false,
    gotMetadata = false;

// image sent to Python
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext("2d");

// image displayed in HTML
let drawCanvas = document.createElement('canvas');
document.body.appendChild(drawCanvas);
let drawCtx = drawCanvas.getContext("2d");

//Starting events
// check if metadata is ready - we need the video size
v.onloadedmetadata = () => {
    console.log("video metadata ready");
    gotMetadata = true;
    if(isPlaying)
        startHandDetection();
};

// see if the video has started playing
v.onplaying = () => {
    console.log("video playing");
    isPlaying = true;
    if(gotMetadata){
        startHandDetection();
    }
};

//Start object detection
function startHandDetection(){
    console.log("starting hand detection");

    // Set canvas sizes based on input video
    drawCanvas.width = v.videoWidth;
    drawCanvas.height = v.videoHeight;

    imageCanvas.width = uploadWidth;
    imageCanvas.height = uploadWidth * (v.videoHeight / v.videoWidth);

    drawCtx.lineWidth = "4";
    drawCtx.strokeStyle = "cyan";
    drawCtx.font ="20px Verdana";
    drawCtx.fillStyle = "cyan";

    //Save and send the first image
    imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoHeight / v.videoWidth));
    imageCanvas.toBlob(postFile, 'image/jpeg');
}

// Add file to blob to a form and post
function postFile(file){
    // Set options as form data
    let formdata = new FormData();
    formdata.append("image", file);
    formdata.append("threshold", scoreThreshold);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.origin + '/prediction', true);
    xhr.onload = function(){
        if(this.status === 200){
            let prediction = this.response;
            console.log(prediction);
            drawResult(prediction);
            $('#result').text(prediction);
            imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoHeight / v.videoWidth));
            imageCanvas.toBlob(postFile, 'image/jpeg');
        }
        else{
            console.error(xhr);
        }
    };
    xhr.send(formdata);
}

function drawResult(prediction){
    //filter out objects that contain a class_name and then draw boxes and labels on each
    drawCtx.fillText("Prediction is " + prediction, 650, 650);
    drawCtx.strokeRect(0, 0, 480, 480);
}



