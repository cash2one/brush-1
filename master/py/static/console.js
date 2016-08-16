// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

var chosen = [];
function getSelectedID() {
    var selected = [];
    chosen.forEach(function(ele){
        var id = ele.split("|")[0];
        var address = ele.split("|")[1];
        console.log(id);
        console.log(address);
        selected.push(id)
    });
    return selected
}

$(document).ready(function() {
    var url = "ws://localhost:8888/console";


//    var chosen = [];
    $('input[type="checkbox"]').change(function() {
     if(this.checked) {
         // do something when checked
         chosen.push(this.value)
         console.log(chosen)

     }
     else if (!this.check) {
        var index = chosen.indexOf(this.value);
        if (index > -1) {
            chosen.splice(index, 1);
            console.log(chosen)
        }
     }

    });

//    function getSelectedID() {
//        var selected = [];
//        chosen.forEach(function(ele){
//            var id = ele.split("|")[0];
//            var address = ele.split("|")[1];
//            console.log(id);
//            console.log(address);
//            selected.push(id)
//        });
//        return selected
//    }

    $("form#upload").submit(function () {
        var selected = getSelectedID();
        console.log(selected)
        if (selected.length == 0) {
            alert("no device selected")
        };
        $("input#selected-ids").val(selected);
    });

    $(".stop-btn").click(function(){
        var selected = getSelectedID();
        console.log(selected);
        if (selected.length == 0) {
            alert("no device selected")
        }
        $.ajax({
            type: "POST",
            url: "stop",
            data: JSON.stringify({
                "ids": selected,
            }),
//            contentType: "application/x-www-form-urlencoded",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(r){
                console.log(r)
            }
        })

    });

    $(".run-btn").click(function(){
        var selected = getSelectedID();
        console.log(selected);
        if (selected.length == 0) {
            alert("no device selected")
        }
        $.ajax({
            type: "POST",
            url: "run",
            data:JSON.stringify({
                "ids": selected,
                "script": $(".script-to-run").val()
            }),
//            contentType: "application/x-www-form-urlencoded; charset=utf-8",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(r){
                console.log(r)
            }
        })

    });

    var ws = new WebSocket(url);
    ws.onmessage = function(event) {
        var msg = JSON.parse(event.data);
        console.log(msg);
    }

});

function showMessage(str) {
    $("body").append("<p>" + str + "<\p>")
}

function openTerminal(id){
    var url = "http://localhost:8888/terminal?id=" + id;
    window.open(url)
}



