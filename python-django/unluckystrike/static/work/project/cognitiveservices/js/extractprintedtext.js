'use strict';

function extractPrintedTextImage() {
    document.getElementById("tooltipTI").style.display = "none";
    // **********************************************
    // *** Update or verify the following values. ***
    // **********************************************

    // Replace <Subscription Key> with your valid subscription key.
    var subscriptionKey = "#";

    // You must use the same Azure region in your REST API method as you used to
    // get your subscription keys. For example, if you got your subscription keys
    // from the West US region, replace "westcentralus" in the URL
    // below with "westus".
    //
    // Free trial subscription keys are generated in the "westus" region.
    // If you use a free trial subscription key, you shouldn't need to change
    // this region.
    var uriBase =
        "https://eastasia.api.cognitive.microsoft.com/vision/v2.0/ocr";

    // Request parameters.
    var params = {
        "language": "en",
        "detectOrientation": "true",
    };

    // Display the image.
    var sourceImageUrl = document.getElementById("inputTextImage").value;
    //document.querySelector("#sourceTextImage").src = sourceImageUrl;

    var image = new Image();       
        image.onload = function() {
            // When image loaded, you can then draw it on the canvas.
            document.getElementById("sourceTextImage").width=image.width*(500/image.width);
            document.getElementById("sourceTextImage").height=image.height*(500/image.width);
            document.getElementById("sourceTextImage").getContext('2d').drawImage(image, 0, 0,image.width*(500/image.width),image.height*(500/image.width));
        };        
        image.src=sourceImageUrl; 

    // Perform the REST API call.
    $.ajax({
        url: uriBase + "?" + $.param(params),

        // Request headers.
        beforeSend: function(jqXHR){
            jqXHR.setRequestHeader("Content-Type","application/json");
            jqXHR.setRequestHeader("Ocp-Apim-Subscription-Key", subscriptionKey);
        },

        type: "POST",

        // Request body.
        data: '{"url": ' + '"' + sourceImageUrl + '"}',
    })

    .done(function(data) {
        // Show formatted JSON on webpage.
        $("#responseResultTextArea").val(JSON.stringify(data, null, 2));

        for (var i = 0; i < data.regions[0].lines.length; i++) {
            var response = data;

            for (var j = 0; j < response.regions[0].lines[i].words.length; j++) {
                var strArray = response.regions[0].lines[i].words[j].boundingBox.split(',');
                var sLeft = parseInt(strArray[0]);
                var sTop = parseInt(strArray[1]);
                var sWidth = parseInt(strArray[2]);
                var sHeight = parseInt(strArray[3]);

                document.getElementById("sourceTextImage").getContext('2d').strokeStyle="orange";
                document.getElementById("sourceTextImage").getContext('2d').lineWidth=2;
                document.getElementById("sourceTextImage").getContext('2d').strokeRect(sLeft*(500/image.width), sTop*(500/image.width), sWidth*(500/image.width), sHeight*(500/image.width));
            }

            // var strArray = response.regions[0].lines[i].boundingBox.split(',');
            // var sLeft = parseInt(strArray[0]);
            // var sTop = parseInt(strArray[1]);
            // var sWidth = parseInt(strArray[2]);
            // var sHeight = parseInt(strArray[3]);


            // document.getElementById("sourceTextImage").getContext('2d').strokeStyle="orange";
            // document.getElementById("sourceTextImage").getContext('2d').lineWidth=2;
            // document.getElementById("sourceTextImage").getContext('2d').strokeRect(sLeft*(500/image.width), sTop*(500/image.width), sWidth*(500/image.width), sHeight*(500/image.width));
        }

        document.getElementById("sourceTextImage").addEventListener("mousemove", on_mousemove, false);

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

                for (var i = 0; i < data.regions[0].lines.length; i++) {
                    var response = data;

                    for (var j = 0; j < response.regions[0].lines[i].words.length; j++) {
                        var strArray = response.regions[0].lines[i].words[j].boundingBox.split(',');

                        var xxx = parseInt(strArray[0]);
                        var yyy = parseInt(strArray[1]);
                        var zzz = parseInt(strArray[2]);
                        var kkk = parseInt(strArray[3]);

                        var linkX = xxx*(500/image.width);
                        var linkY = yyy*(500/image.width);
                        var linkWidth = zzz*(500/image.width);
                        var linkHeight = kkk*(500/image.width);
                    if (x >= linkX && x <= (linkX + linkWidth) && y >= linkY && y <= (linkY + linkHeight)){
                        document.getElementById("tooltipTI").style.display = "";
                        document.getElementById("tooltipTI").style.left = getPosition(document.getElementById("sourceTextImage")).x + linkX + "px";
                        document.getElementById("tooltipTI").style.top = getPosition(document.getElementById("sourceTextImage")).y + linkY + linkHeight + 10+ "px";
                        document.getElementById("tooltipTI").getContext('2d').clearRect(0, 0, document.getElementById("tooltipTI").width, document.getElementById("tooltipTI").height); 
                        document.getElementById("tooltipTI").getContext('2d').textAlign="right";
                        document.getElementById("tooltipTI").getContext('2d').textBaseline = 'middle';
                        document.getElementById("tooltipTI").getContext('2d').font= "24px Consolas";
                        document.getElementById("tooltipTI").getContext('2d').fillText(response.regions[0].lines[i].words[j].text, 125, 25, 250);
                        break;
                    }
                    else {
                        document.getElementById("tooltipAI").style.display = "none";
                    }
                }
            };
        }
    })

    .fail(function(jqXHR, textStatus, errorThrown) {
        // Display error message.
        var errorString = (errorThrown === "") ?
            "Error. " : errorThrown + " (" + jqXHR.status + "): ";
        errorString += (jqXHR.responseText === "") ? "" :
            (jQuery.parseJSON(jqXHR.responseText).message) ?
                jQuery.parseJSON(jqXHR.responseText).message :
                jQuery.parseJSON(jqXHR.responseText).error.message;
        alert(errorString);
    });
};