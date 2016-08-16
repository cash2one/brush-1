var fs = require('fs');
var express = require('express'),
    multer  = require('multer'),
    bodyParser = require('body-parser');
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);

var swig = require('swig');

app.engine('html', swig.renderFile);

app.set('view engine', 'html');
app.set('views', __dirname + '/templates');
app.use(express.static('static'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));
//app.use(multer({ dest: './uploads/'}));
var uploading = multer({ dest: './uploads'});

var devices = [{id: 1, address: '127.0.0.1'}, {id: 2, address: '127.0.0.2'}, {id: 3, address: '127.0.0.3'}]
var Devices = {};

function getSeletedDevices(selectedIds){
  console.log("selectedIds: " + selectedIds);
  var dd = [];
  for (k in Devices){ dd.push(Devices[k]); }
  var selected = dd.filter(function(ele){
    return (selectedIds.indexOf(ele.id) == -1)?false:true;
  })
  return selected
}
app.get('/', function (req, res) {
//   res.render('index', { devices: devices });
//   console.log(Devices)
   var dd = [];
   for (k in Devices){ dd.push(Devices[k]); }
   res.render('index', { devices: dd});
});

app.post('/fileproxy', uploading.single("file"), function(req, res){
  console.log("file upload");
  console.log(req.body);
  var ids = req.body.ids.split(',');
  console.log(req.file);
  var tmp_path = req.file.path;
  var filename = req.file.originalname;
  var raw = fs.readFileSync(tmp_path);
  var content = raw.toString('base64');
//  console.log(content);
//  var dd = [];
//  for (k in Devices){ dd.push(Devices[k]); }
//  console.log(dd)
  var dd = getSeletedDevices(ids);
  dd.forEach(function(ele){
    console.log("send file to " + ele.id)
    ele.ws.emit('upload', {filename: filename, payload: content})
  });

  fs.unlinkSync(tmp_path);
  res.redirect('/');
});

app.post('/run', function(req, res){
  console.log(req.body)
  var ids = req.body.ids;
  var script = req.body.script;

  var selectedDevices = getSeletedDevices(ids);
  selectedDevices.forEach(function(ele){
    ele.ws.emit("run_script", {script: script});
  });
  console.log("run");
});

app.post('/stop', function(req, res){

  console.log(req.body)
  var ids = req.body.ids

  var selectedDevices = getSeletedDevices(ids);
  selectedDevices.forEach(function(ele){
    ele.ws.emit("stop_script", {});
  });
  console.log(selectedDevices);
  console.log("stop");
});

app.get('/terminal', function(req, res){
  console.log("open terminal");
  res.render('terminal', {id: 18});
})

io.on('connection', function (socket) {
  var clientIp = socket.request.connection.remoteAddress;
  console.log(socket.id);
  console.log('New connection from ' + clientIp);

   var dev = {
        id: socket.id,
        address: clientIp,
        ws: socket
   }
   socket.uid = socket.id;
   Devices[socket.uid] = dev;

  socket.emit('news', { hello: 'world' });
  socket.on('event', function (data) {
    console.log(data);
  });

  socket.on("reg", function(data){
    delete Devices[socket.uid];
    var dev = {
        id: data,
        address: socket.request.connection.remoteAddress,
        ws: socket
    }
    socket.uid = data;
    Devices[socket.uid] = dev;


  });

  socket.on('disconnect', function () {
    console.log("we lost 1 man");
    delete Devices[socket.uid];
  });

});


server.listen(4000, function(){
  var host = server.address().address;
  var port = server.address().port;

  console.log('App listening at http://%s:%s', host, port);
});
