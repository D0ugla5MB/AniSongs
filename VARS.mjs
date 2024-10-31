import { getUrlsList } from "./utils_page.mjs";

//temp var: will be recplaced by env vars
const FILES_PATH = {
    animes_url: '/anime_links.txt',
    url_query_limit: '/numeric_parts.txt'
};
const URL_BASE = "https://myanimelist.net/topanime.php?limit=";
const PORT = 3000;
const MAX_PAGES = 1;

const SELECTORS = {
    animeTitle: {
        parentTagTitle: 'h1',
        classTitle: 'title-name',
        titleTag: 'strong'
    },
    songContainer: {
        container: 'div',
        classOpening: 'opnening', //the class name has this misstype
        classEnding: 'ending'
    },
    songDetails: {
        index: 'span.theme-song-index',
        title: 'span.theme-song-title',
        artist: 'span.theme-song-artist'
    }
};

const LAST_FETCHED_PAGE = '';
const URLS_LIST = getUrlsList(FILES_PATH.animes_url);


export function getUrlBase() { return URL_BASE; }
export function getServerPort() { return PORT; }
export function getMaxPages() { return MAX_PAGES; }
export function getAnimeTitleElemSelector() { return SELECTORS.animeTitle; }
export function getSongContainerSelector() { return SELECTORS.songContainer; }
export function getSongDetailsSelector() { return SELECTORS.songDetails; }
export function getAllSelectors() {
    return {
        title: getAnimeTitleElemSelector(),
        song_div: getSongContainerSelector(),
        details: getSongDetailsSelector()
    }
}
export function getFilesPath(){return FILES_PATH;}