import https from 'https';
import * as cheerio from 'cheerio';
import fs from 'fs';
import { getQueryLimitNum } from './utils_page.mjs';
import { getUrlBase, getMaxPages } from './VARS.mjs';


function createPageTracker() {
    let totalFetchedPages = 0;

    return {
        getCurrentPage: () => totalFetchedPages,
        incrementPage: () => { totalFetchedPages += 1; },
        resetPage: () => { totalFetchedPages = 0; }
    };
}

const pageTracker = createPageTracker();
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
const queryLimitRange = () => 50 * pageTracker.getCurrentPage();

export function getQueryLimitNum(num) {
    const subStr = num.match(/\d+/);
    return subStr ? parseInt(subStr[0], 10) : 0;
}

export function getUrlsList(urlsListFile) {
    try {
        const data = fs.readFileSync(urlsListFile, 'utf8');

        return data
            .split('\n')
            .map(url => url.trim())
            .map(url => {
                const urlAux = new URL(url);
                const limitQuery = urlAux.searchParams.get('limit') || null;
                const typeQuery = urlAux.searchParams.get('type') || null;
                const otherQueries = Array.from(urlAux.searchParams.entries())
                    .filter(([key]) => key !== 'limit' && key !== 'type')
                    .map(([key, value]) => `${key}=${value}`);

                return {
                    fullUrl: url,
                    baseUrl: urlAux.origin + urlAux.pathname,
                    limitQuery: limitQuery,
                    typeQuery: typeQuery,
                    otherQueries
                };
            });
    } catch (error) {
        console.error('Error reading file:', error);
        throw error;
    }
}

export function fetchPage(url, retries = 3) {
    return new Promise((resolve, reject) => {
        let bodyContent = '';
        https.get(url, async (response) => {
            const { statusCode } = response;
            if (statusCode === 404) {
                console.log(`${statusCode}`);
                return resolve(null);
            } else if (statusCode !== 200) {
                console.error(`Request failed with status code: ${statusCode}`);
                if (retries > 0) {
                    console.log(`Retrying... attempts left: ${retries}`);
                    await delay(2000);
                    return resolve(fetchPage(url, retries - 1));
                }
                return reject(new Error(`Request failed with status code: ${statusCode}`));
            }
            response.on('data', (chunk) => {
                bodyContent += chunk;
            });

            response.on('end', () => {
                resolve(bodyContent);
            });
        }).on('error', async (err) => {
            if (retries > 0) {
                console.log(`Retrying due to error: ${err.message}`);
                await delay(2000);
                return resolve(fetchPage(url, retries - 1));
            }
            reject(err);
        });
    });
}

function scrapAnchorHref(html) {
    const $ = cheerio.load(html);
    const anchorTags = $('a:has(img)').filter((i, elem) => {
        const href = $(elem).attr('href');
        return href && /myanimelist\.net\/anime\/\d+\//.test(href);
    });

    const urls = [];
    if (anchorTags.length > 0) {
        anchorTags.each((i, el) => {
            $(el).find('img').remove();
        });

        urls.push(...anchorTags.map((i, elem) => $(elem).attr('href')).get());
        console.log(`Found ${urls.length} valid links.`);
    } else {
        console.log("No anchor tags found.");
    }

    return urls;
}

function saveUrls(urlsList) {
    fs.appendFileSync('anime_links.txt', urlsList.join('\n') + '\n');
    console.log(`Stored ${urlsList.length} links to file.`);
}

function saveUrlsNumParts(urlsList) {
    let arrNums = '';

    for (let url of urlsList) {
        const nums = url.match(/\/(\d+)\//);
        if (nums) {
            arrNums += nums[1] + '~';
        }
    }
    arrNums = arrNums.slice(0, -1);

    fs.appendFileSync('numeric_parts.txt', arrNums);
}

async function loadPages() {
    while (pageTracker.getCurrentPage() < getMaxPages()) {
        let MAL_URL_BASE = `${getUrlBase()}${queryLimitRange()}`;
        console.log(`Fetching page: ${MAL_URL_BASE}`);

        pageTracker.incrementPage();

        const html = await fetchPage(MAL_URL_BASE);
        if (!html) { break; }

        const linksList = scrapAnchorHref(html);
        linksList.sort((f, s) => getQueryLimitNum(f) - getQueryLimitNum(s));
        saveUrls(linksList);
        saveUrlsNumParts(linksList);
        await delay(1000);
    }
}

export function getHtmlContent() {
    loadPages().catch(err => console.error(err));

}
