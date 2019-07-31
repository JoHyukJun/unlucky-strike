
	
    'use strict';
    
    function processImage() {
        document.getElementById("tooltip").style.display = "none";
        // **********************************************
        // *** Update or verify the following values. ***
        // **********************************************

        // Replace the subscriptionKey string value with your valid subscription key.
        var subscriptionKey = "db51abe115734df19ce4c82cd538fd7b";

        // Replace or verify the region.
        //
        // You must use the same region in your REST API call as you used to obtain your subscription keys.
        // For example, if you obtained your subscription keys from the westus region, replace
        // "westcentralus" in the URI below with "westus".
        //
        // NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
        // a free trial subscription key, you should not need to change this region.
        var uriBase = "https://eastasia.api.cognitive.microsoft.com/face/v1.0/detect";

        // Request parameters.
        var params = {
            "returnFaceId": "true",
            "returnFaceLandmarks": "false",
            "returnFaceAttributes": "age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise",
        };

        // Display the image.
        var sourceImageUrl = document.getElementById("inputImage").value;
        //document.querySelector("#sourceImage").src = sourceImageUrl;

        var image = new Image();       
        image.onload = function() {
            // When image loaded, you can then draw it on the canvas.
            document.getElementById("sourceImage").width=image.width*(500/image.width);
            document.getElementById("sourceImage").height=image.height*(500/image.width);
            document.getElementById("sourceImage").getContext('2d').drawImage(image, 0, 0,image.width*(500/image.width),image.height*(500/image.width));
        };        
        image.src=sourceImageUrl; 

        // Perform the REST API call.
        $.ajax({
            url: uriBase + "?" + $.param(params),

            // Request headers.
            beforeSend: function(xhrObj){
                xhrObj.setRequestHeader("Content-Type","application/json");
                xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key", subscriptionKey);
            },

            type: "POST",

            // Request body.
            data: '{"url": ' + '"' + sourceImageUrl + '"}',
        })

        .done(function(data) {
            $("#responseTextArea").val(JSON.stringify(data, null, 2));

            for (var i = 0; i < data.length; i++) {
                var response = data[i];

                document.getElementById("sourceImage").getContext('2d').strokeStyle="orange";
                document.getElementById("sourceImage").getContext('2d').lineWidth=2;
                document.getElementById("sourceImage").getContext('2d').strokeRect(response.faceRectangle.left*(500/image.width), response.faceRectangle.top*(500/image.width), response.faceRectangle.width*(500/image.width), response.faceRectangle.height*(500/image.width));
            }

            document.getElementById("sourceImage").addEventListener("mousemove", on_mousemove, false);

            function getPosition (element) {
                var x = 0;
                var y = 0;

                while (element) {
                    x += element.offsetLeft - element.scrollLeft + element.clientLeft;
                    y += element.offsetTop - element.scrollLeft + element.clientTop;
                    element =  element.offsetParent;
                }

                return { x: x, y: y };
            }

            function on_mousemove (ev) {
                var x, y;

                if (ev.layerX || ev.layerX == 0) {
                    x = ev.layerX;
                    y = ev.layerY;
                }

                for (var i = 0; i < data.length; i++) {
                    var response = data[i];
                    var linkX = response.faceRectangle.left*(500/image.width);
                    var linkY = response.faceRectangle.top*(500/image.width);
                    var linkWidth = response.faceRectangle.width*(500/image.width);
                    var linkHeight = response.faceRectangle.height*(500/image.width);
                    if (x >= linkX && x <= (linkX + linkWidth) && y >= linkY && y <= (linkY + linkHeight)){
                        document.getElementById("tooltip").style.display = "";
                        document.getElementById("tooltip").style.left = getPosition(document.getElementById("sourceImage")).x + linkX + "px";
                        document.getElementById("tooltip").style.top = getPosition(document.getElementById("sourceImage")).y + linkY + linkHeight + 10+ "px";
                        document.getElementById("tooltip").getContext('2d').clearRect(0, 0, document.getElementById("tooltip").width, document.getElementById("tooltip").height); 
                        document.getElementById("tooltip").getContext('2d').textAlign="center";
                        document.getElementById("tooltip").getContext('2d').textBaseline = 'middle';
                        document.getElementById("tooltip").getContext('2d').font= "24px Consolas";
                        document.getElementById("tooltip").getContext('2d').fillText("Gender: " + response.faceAttributes.gender+"  Age: " + response.faceAttributes.age, 125, 25, 250);
                        document.getElementById("tooltip").getContext('2d').fillText("/*Emotion*/", 125, 50, 250);
                        document.getElementById("tooltip").getContext('2d').fillText("Anger: " + response.faceAttributes.emotion.anger+" Contempt: " + response.faceAttributes.emotion.contempt, 125, 75, 250);
                        document.getElementById("tooltip").getContext('2d').fillText("Disgust: " + response.faceAttributes.emotion.disgust+" Fear: " + response.faceAttributes.emotion.fear, 125, 100, 250);
                        document.getElementById("tooltip").getContext('2d').fillText("Happiness: " + response.faceAttributes.emotion.happiness+" Neutral: " + response.faceAttributes.emotion.neutral, 125, 125, 250);
                        document.getElementById("tooltip").getContext('2d').fillText("Sadness: " + response.faceAttributes.emotion.sadness+" Surprise: " + response.faceAttributes.emotion.surprise, 125, 150, 250);

                        break;
                    }
                    else {
                        document.getElementById("tooltip").style.display = "none";
                    }
                };
            }
        })

        .fail(function(jqXHR, textStatus, errorThrown) {
            // Display error message.
            var errorString = (errorThrown === "") ? "Error. " : errorThrown + " (" + jqXHR.status + "): ";
            errorString += (jqXHR.responseText === "") ? "" : (jQuery.parseJSON(jqXHR.responseText).message) ? 
                jQuery.parseJSON(jqXHR.responseText).message : jQuery.parseJSON(jqXHR.responseText).error.message;
            alert(errorString);
        });
    };