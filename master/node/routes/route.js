var fs = require('fs');

function getSeletedDevices(selectedIds){
  console.log("selectedIds: " + selectedIds);
  var dd = [];
  for (k in Devices){ dd.push(Devices[k]); }
  var selected = dd.filter(function(ele){
    return (selectedIds.indexOf(ele.id) == -1)?false:true;
  })
  return selected
}

exports.index = function (req, res) {
//   res.render('index', { devices: devices });
//   console.log(Devices)
   var dd = [];
   for (k in Devices){ dd.push(Devices[k]); }
   res.render('index', { devices: dd});
};

exports.fileUpload = function(req, res){
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
};

exports.runScript = function(req, res){
  console.log(req.body)
  var ids = req.body.ids;
  var script = req.body.script;

  var selectedDevices = getSeletedDevices(ids);
  selectedDevices.forEach(function(ele){
    ele.ws.emit("run_script", {script: script});
  });
  console.log("run");
};

exports.stopScript = function(req, res){
  console.log(req.body)
  var ids = req.body.ids

  var selectedDevices = getSeletedDevices(ids);
  selectedDevices.forEach(function(ele){
    ele.ws.emit("stop_script", {});
  });
  console.log("stop");
};

exports.terminal = function(req, res){
  console.log("open terminal");
  res.render('terminal', {id: 18});
};
