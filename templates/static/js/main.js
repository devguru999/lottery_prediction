$(document).ready(() => {
    $("#area-box").change(() => {
        fetch('/lottery', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({area_code: $("#area-box").val()}) 
        })
        .then(response => response.json())
        .then(data => {
            $("#lottery-box").empty();
            $("#lottery-box").append($('<option>', {
                value: "",
                text: "-- select type --",
            }));
            data.forEach((item) => {
                $("#lottery-box").append($('<option>', {
                    value: item,
                    text: item
                }));
            });            
        })
        .catch(error => {
            console.error(error);
        });
    });

    $("#lottery-box").change(() => {
        fetch('/data', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                area_code: $("#area-box").val(), 
                lottery: $("#lottery-box").val()
            }) 
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.length)
            $("#lotto-values").empty();
            data.forEach((item, index) => {
                $("#lotto-values").append($('<option>', {
                    value: index,
                    text: JSON.stringify(item)
                }));
            });   
        })
        .catch(error => {
            console.error(error);
        });
    });

    $("a#predict").click(() => {
        fetch('/predict', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                area_code: $("#area-box").val(), 
                lottery: $("#lottery-box").val()
            }) 
        })
        .then(response => response.json())
        .then(data => {
            $("#prediction").empty();
            data.forEach((item) => {
                $("#prediction").append($('<div>', {
                    text: item
                }))
            })
        })
        .catch(error => {
            console.error(error);
        });
    });
})