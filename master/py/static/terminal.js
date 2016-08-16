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

$(document).ready(function() {
    var url = "ws://" + document.URL.split("/")[2]+ "/proxy?id=" + clientID;
    var ws = new WebSocket(url);
    ws.onmessage = function(event) {
        showMessage(event.data);
    }
});

function showMessage(str){
    $("body").append("<p>" + str + "<\p>");
    var h = $(document).height()-$(window).height();
    window.scroll(0, h);
}

