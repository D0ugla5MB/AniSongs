import { fetchPage } from "./db_data.mjs";
import fs from 'fs';
import path from 'path';

function getUrlsFromFile(fileName) {
    const filePath = path.resolve(fileName);
    const data = fs.readFileSync(filePath, 'utf-8');
    return data.split('\n').filter((url) => url.trim().length > 0);
}

async function fetchUrlsContent(filename) {
    const urls = getUrlsFromFile(filename);
    const htmlContents = [];

    for (const url of urls) {
        const htmlContent = await fetchPage(url);
        if (htmlContent) {
            htmlContents.push({ url, content: htmlContent });
            console.log(`Fetched and stored content for ${url}`);
        } else {
            console.log(`No content found for ${url}`);
        }
    }

    return htmlContents;
}
//need to dealt with pieces of info
function scrapeThemeSongData(htmlContent) {
    const $ = cheerio.load(htmlContent);
    const themeSongs = {
       
    };


    return themeSongs;
}
