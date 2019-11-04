'use strict';

function analyzeImage() {
    document.getElementById("tooltipAI").style.display = "none";
    // **********************************************
    // *** Update or verify the following values. ***
    // **********************************************

    // Replace <Subscription Key> with your valid subscription key.
    var subscriptionKey = "ff85de274e2948a78fb11262d375a782";

    // You must use the same Azure region in your REST API method as you used to
    // get your subscription keys. For example, if you got your subscription keys
    // from the West US region, replace "westcentralus" in the URL
    // below with "westus".
    //
    // Free trial subscription keys are generated in the "westus" region.
    // If you use a free trial subscription key, you shouldn't need to change
    // this region.
    var uriBase =
        "https://eastAsia.api.cognitive.microsoft.com/vision/v2.0/analyze";

    // Request parameters.
    var params = {
        "visualFeatures": "Categories,Description,Color",
        "details": "",
        "language": "en",
    };

    // Display the image.
    var sourceImageUrl = document.getElementById("inputAnalyzeImage").value;
    //document.querySelector("#sourceAnalyzeImage").src = sourceImageUrl;


    var image = new Image();       
        image.onload = function() {
            // When image loaded, you can then draw it on the canvas.
            document.getElementById("sourceAnalyzeImage").width=image.width*(500/image.width);
            document.getElementById("sourceAnalyzeImage").height=image.height*(500/image.width);
            document.getElementById("sourceAnalyzeImage").getContext('2d').drawImage(image, 0, 0,image.width*(500/image.width),image.height*(500/image.width));
        };        
        image.src=sourceImageUrl; 

    // Make the REST API call.
    $.ajax({
        url: uriBase + "?" + $.param(params),

        // Request headers.
        beforeSend: function(xhrObj){
            xhrObj.setRequestHeader("Content-Type","application/json");
            xhrObj.setRequestHeader(
                "Ocp-Apim-Subscription-Key", subscriptionKey);
        },

        type: "POST",

        // Request body.
        data: '{"url": ' + '"' + sourceImageUrl + '"}',
    })

    .done(function(data) {
        // Show formatted JSON on webpage.
        $("#responseAnalyzeTextArea").val(JSON.stringify(data, null, 2));


        for (var i = 0; i < data.categories[0].detail.celebrities.length; i++) {
            var response = data;

            document.getElementById("sourceAnalyzeImage").getContext('2d').strokeStyle="orange";
            document.getElementById("sourceAnalyzeImage").getContext('2d').lineWidth=2;
            document.getElementById("sourceAnalyzeImage").getContext('2d').strokeRect(response.categories[0].detail.celebrities[i].faceRectangle.left*(500/image.width), response.categories[0].detail.celebrities[i].faceRectangle.top*(500/image.width), response.categories[0].detail.celebrities[i].faceRectangle.width*(500/image.width), response.categories[0].detail.celebrities[i].faceRectangle.height*(500/image.width));
        }

        document.getElementById("sourceAnalyzeImage").addEventListener("mousemove", on_mousemove, false);

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

                for (var i = 0; i < data.categories[0].detail.celebrities.length; i++) {
                    var response = data;
                    var linkX = response.categories[0].detail.celebrities[i].faceRectangle.left*(500/image.width);
                    var linkY = response.categories[0].detail.celebrities[i].faceRectangle.top*(500/image.width);
                    var linkWidth = response.categories[0].detail.celebrities[i].faceRectangle.width*(500/image.width);
                    var linkHeight = response.categories[0].detail.celebrities[i].faceRectangle.height*(500/image.width);
                    if (x >= linkX && x <= (linkX + linkWidth) && y >= linkY && y <= (linkY + linkHeight)){
                        document.getElementById("tooltipAI").style.display = "";
                        document.getElementById("tooltipAI").style.left = getPosition(document.getElementById("sourceAnalyzeImage")).x + linkX + "px";
                        document.getElementById("tooltipAI").style.top = getPosition(document.getElementById("sourceAnalyzeImage")).y + linkY + linkHeight + 10+ "px";
                        document.getElementById("tooltipAI").getContext('2d').clearRect(0, 0, document.getElementById("tooltipAI").width, document.getElementById("tooltipAI").height); 
                        document.getElementById("tooltipAI").getContext('2d').textAlign="center";
                        document.getElementById("tooltipAI").getContext('2d').textBaseline = 'middle';
                        document.getElementById("tooltipAI").getContext('2d').font= "24px Consolas";
                        document.getElementById("tooltipAI").getContext('2d').fillText("Name: " + response.categories[0].detail.celebrities[i].name, 125, 25, 250);
                        break;
                    }
                    else {
                        document.getElementById("tooltipAI").style.display = "none";
                    }
                };
            }
    })

    .fail(function(jqXHR, textStatus, errorThrown) {
        // Display error message.
        var errorString = (errorThrown === "") ? "Error. " :
            errorThrown + " (" + jqXHR.status + "): ";
        errorString += (jqXHR.responseText === "") ? "" :
            jQuery.parseJSON(jqXHR.responseText).message;
        alert(errorString);
    });
};