# Proxy Bypasser

Provides a HTTP server which serves a directory of files, 
which can be downloaded via JavaScript. They will be zipped. Indicated filetype is PDF (not really relevant). 

Proxies are blind for this technique. 


## Usage

```
$ pip install -r requirements.txt
$ python3 proxybypasser.py --path /mnt/data
```


## What?

Content of file is in `{{filecontent}}` inside a javascript variable inside a 
html. No HTTP request to the file is being performed, its all in the browser. 

`download.html`:
```javascript
<script>
    function download() {
        const linkSource = `data:application/pdf;base64,{{filecontent}}`;
        const downloadLink = document.createElement('a');
        document.body.appendChild(downloadLink);
    
        downloadLink.href = linkSource;
        downloadLink.target = '_self';
        downloadLink.download = "{{filename}}";
        downloadLink.click(); 
    }
</script>
```