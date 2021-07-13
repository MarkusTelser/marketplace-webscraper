
    function deleteRow(btn) {
        var row = btn.parentNode.parentNode;
        var link = row.getElementsByTagName("td")[0].childNodes[0].getAttribute("href");
        
        // remove html column
        row.parentNode.removeChild(row);
    }
    