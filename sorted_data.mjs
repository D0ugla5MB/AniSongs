export function getQueryLimitNum(num) {
    const subStr = num.match(/\d+/);
    return subStr ? parseInt(subStr[0], 10) : 0;
}