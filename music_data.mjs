import { fetchPage } from "./db_data.mjs";
import fs from 'fs';
import path from 'path';
import * as cheerio from 'cheerio';

const SELECTORS = {
    animeTitle: {
        parentTagTitle: 'h1',
        classTitle: 'title-name',
        titleTag: 'strong'
    },
    themeSongContainer: {
        container: 'div',
        classOpening: 'opnening', //the class name has this misstype
        classEnding: 'ending'
    },
    themeSongDetails: {
        index: 'span.theme-song-index',
        title: 'span.theme-song-title',
        artist: 'span.theme-song-artist'
    }
};

function getUrlsFromFile(fileName) {
    const filePath = path.resolve(fileName);
    const data = fs.readFileSync(filePath, 'utf-8'); //blocking operation
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
    const themeSongs = [];

    const animeTitleElem = $(`${SELECTORS.animeTitle.parentTagTitle}[class*="${SELECTORS.animeTitle.classTitle}"] ${SELECTORS.animeTitle.titleTag}`);
    const animeTitle = animeTitleElem.text().trim();

    $(`${SELECTORS.themeSongContainer.container}[class*="${SELECTORS.themeSongContainer.classOpening}"], ${SELECTORS.themeSongContainer.container}[class*="${SELECTORS.themeSongContainer.classEnding}"]`).each((_, opORed) => {
        const type = $(opORed).attr('class').includes(SELECTORS.themeSongContainer.classOpening) ? 'opening' : 'ending';

        $(opORed).find(SELECTORS.themeSongDetails.index).each((i, songElem) => {
            const index = $(songElem).text().trim();
            const titleElement = $(opORed).find(SELECTORS.themeSongDetails.title).eq(i);
            const title = titleElement.length ? titleElement.text().trim() : $(opORed).text().trim();
            const artist = $(opORed).find(SELECTORS.themeSongDetails.artist).eq(i).text().trim();

            themeSongs.push({
                index,
                title,
                artist,
                anime: animeTitle,
                type
            });
        });
    });

    return themeSongs;
}

export async function getThemeSongsData() {
    const filename = 'anime_links.txt'; 
    const htmlContents = await fetchUrlsContent(filename);

    for (const { url, content } of htmlContents) {
        const themeData = scrapeThemeSongData(content);
        console.log(`Data for ${url}:`, themeData);
    }
}