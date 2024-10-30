import { fetchPage } from "./db_data.mjs";
import fs from 'fs';
import path from 'path';
import * as cheerio from 'cheerio';
import { getAllSelectors as SELECTORS } from "./VARS.mjs";

function getUrlsFromFile(fileName) {
    const filePath = path.resolve(fileName);
    const data = fs.readFileSync(filePath, 'utf-8'); // blocking operation
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

function scrapeThemeSongData(htmlContent) {
    const $ = cheerio.load(htmlContent);
    const themeSongs = [];

    const { title: animeTitleSelector, song_div: songContainerSelector, details: songDetailsSelector } = SELECTORS();

    const animeTitleElem = $(
        `${animeTitleSelector.parentTagTitle}[class*="${animeTitleSelector.classTitle}"] 
         ${animeTitleSelector.titleTag}`
    );

    const animeTitle = animeTitleElem.text().trim();

    $(`${songContainerSelector.container}[class*="${songContainerSelector.classOpening}"],
       ${songContainerSelector.container}[class*="${songContainerSelector.classEnding}"]`)
        .each((_, opORed) => {
            const type = $(opORed).attr('class')
                .includes(songContainerSelector.classOpening) ? 'opening' : 'ending';

            $(opORed).find(songDetailsSelector.index).each((i, songElem) => {
                const index = $(songElem).text().trim();
                const titleElement = $(opORed).find(songDetailsSelector.title).eq(i);
                const title = titleElement.length ? titleElement.text().trim() : $(opORed).text().trim();
                const artist = $(opORed).find(songDetailsSelector.artist).eq(i).text().trim();

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
