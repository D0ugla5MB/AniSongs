import http from 'http';
import { getHtmlContent } from './db_data.mjs'; 

const PORT = 3000;

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.write('Check console for progress.\n');
    res.end('Crawling in progress...');
});

server.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
    getHtmlContent(); 
});
