const Folder = "../static/images";
const fs = require("fs");

var content = 'document.getElementById("1").innerHTML = "';
fs.writeFile('../static/read.js', content, err => {
    if(err){
        console.err;
        return;
    }
    fs.readdir(Folder, (err, files) => {
        if(err){
            console.error(err);
            return;
        }
        files.forEach(file => { //for each image file, read its name
            // const content = '<img src=\\"../static/images/' + file + '\\"> '; // add files name to js we will need for our html
            const content = '<label><input type=\\"radio\\" name=\\"image\\" value=\\"' +file+ '\\"required><img src=\\"../static/images/' + file + '\\"></label>';
            fs.appendFileSync('../static/read.js', content, err => {
                if(err){
                    console.err;
                    return;
                }
            });
            console.log(content);
        });
        
        content = '";';
        fs.appendFile('../static/read.js', content, err => {
            if(err){
            console.err;
            return;
        }
    });
    });
    
});