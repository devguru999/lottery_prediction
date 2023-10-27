$(document).ready(() => {
    $("#status").hide();
    $("#area-box").change(() => {
        $("#status").show();
        $("#status").text('getting lotteries ...');
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

            $("#status").hide();
        })
        .catch(error => {
            console.error(error);
            $("#status").hide();
        });
    });

    $("#lottery-box").change(() => {
        $("#status").show();
        $("#status").text('getting winning numbers ...');
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
            $("#status").hide();
        })
        .catch(error => {
            console.error(error);
            $("#status").hide();
        });
    });

    $("a#predict").click(() => {
        $("#status").show();
        $("#status").text('calculating prediction ...');
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
            $("#status").hide();
        })
        .catch(error => {
            console.error(error);
            $("#status").hide();
        });
    });

    $("a#update").click(() => {
        $("#status").show();
        $("#status").text('checking for updates ...');        
        fetch('/check', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.diff_days > 0) {
                $("#status").text('new updates available. updating now ...');       
                fetch('/update', {
                    method: 'POST',                    
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        latest_date: data.latest_date
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);  
                    $("#status").hide();
                })
                .catch(error => {
                    console.error(error);
                    $("#status").hide();
                });
            } else {
                $("#status").hide();
            }
        })
        .catch(error => {
            console.error(error);
            $("#status").hide();
        });
    });
})