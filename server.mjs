import http from 'http';
import { getHtmlContent } from './db_data.mjs';

const PORT = 3000;

const server = http.createServer((req, res) => {

    if (req.url == '/') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.write("<h1>I hope I finish it...</h1");
    } else {
        res.writeHead(res.statusCode, { 'Content-Type': 'text/html' });
        res.write("<h1>I wish :'D</h1>");
    }
    res.end();
}).listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
}).close(getHtmlContent);
