import http from 'http';
import { getHtmlContent } from './db_data.mjs';
import { getThemeSongsData } from './music_data.mjs';
import { getServerPort } from './VARS.mjs';


const server = http.createServer((req, res) => {

    if (req.url == '/') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.write("<h1>I hope I finish it...</h1");
    } else {
        res.writeHead(res.statusCode, { 'Content-Type': 'text/html' });
        res.write("<h1>I wish :'D</h1>");
    }
    res.end();
}).listen(getServerPort(), () => {
    console.log(`Server is running at http://localhost:${PORT}`);
}).close(getThemeSongsData);
