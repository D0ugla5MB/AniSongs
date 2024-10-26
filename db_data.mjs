import https from 'https';
import * as cheerio from 'cheerio';
import fs from 'fs';

function incQueryLimitRange(currentLimit) {
    return () => currentLimit += 50;
}

export function getHtmlContent() {
    let queryLimitRange = incQueryLimitRange(-50);
    const URL_BASE = "https://myanimelist.net/topanime.php?limit=";
    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    const MAX_PAGES = 1;
    let totalFetchedPages = 0;

    const fetchPage = (url, retries = 3) => {
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
    };

    const scrapAnchorHref = (html) => {
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
    };

    const saveUrls = (urlsList) => {
        fs.appendFileSync('anime_links.txt', urlsList.join('\n') + '\n');
        console.log(`Stored ${urlsList.length} links to file.`);
    };

    const loadPages = async () => {
        while (totalFetchedPages < MAX_PAGES) {
            let MAL_URL_BASE = `${URL_BASE}${queryLimitRange()}`;
            console.log(`Fetching page: ${MAL_URL_BASE}`);
            totalFetchedPages += 1;

            const html = await fetchPage(MAL_URL_BASE);
            if (!html) { break; }

            const linksList = scrapAnchorHref(html);
            saveUrls(linksList);

            await delay(1000);
        }
    };

    loadPages().catch(err => console.error(err));
}
