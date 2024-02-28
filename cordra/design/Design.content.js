const TOKEN_ISS = "https://orcid.org";
const TOKEN_AUD = "APP-EM6F9ZHFG0CVCENH";
const USER_OAUTH_PROP = "orcid";


const cordra = require('cordra');
const cordraUtil = require('cordraUtil');


exports.generateId = generateId;
exports.isGenerateIdLoopable = true;

let providerPublicKey = null;
exports.authenticate = authenticate;


/* GENERATE ID */

function generateId(object, context) {
    const prefix = cordra.get('design').content.handleMintingConfig.prefix;
    const p1 = shoulder(object.type);
    const p2 = randomHex(4);
    const p3 = randomHex(4);
    const p4 = randomHex(4);
    return `${prefix}/${p1}-${p2}-${p3}-${p4}`;
}


function shoulder(type) {
    const nonTest = ['c9ce', '485b'];
    const schema = require('/cordra/schemas/' + type + '.schema.json');
    if ('$code' in schema) {
        if (nonTest.includes(schema.$code)) return schema.$code;
        else return 'TEST/' + schema.$code;
    } else {
        return '0000';
    }
}


const randomHex = size => [...Array(size)].map(() => Math.floor(Math.random() * 16).toString(16)).join('');


/* AUTHENTICATE */


function authenticate(authInfo, context) {
    cacheKeyIfNeeded();
    if (isTokenAuthentication(authInfo)) {
        return checkCredentials(authInfo);
    } else {
        return null;
    }
}

function isTokenAuthentication(authInfo) {
    if (authInfo.token) {
        if (isJwtFromProvider(authInfo.token)) {
            return true;
        }
    }
    return false;
}

function isJwtFromProvider(token) {
    if (!token.includes(".")) {
        return false;
    }
    try {
        const claims = cordraUtil.extractJwtPayload(token);
        return TOKEN_ISS === claims.iss;
    } catch (error) {
        return false;
    }
}

function checkCredentials(authInfo) {
    const token = authInfo.token;
    const payload = cordraUtil.extractJwtPayload(token);
    const isVerified = cordraUtil.verifyWithKey(token, providerPublicKey);
    const claimsCheck = checkClaims(payload);
    const active = isVerified && claimsCheck;
    const result = {
        active: active
    };
    if (active) {
        const query = 'type:"CordraUser" AND /' + USER_OAUTH_PROP + ':"' + cordraUtil.escapeForQuery(payload.sub) + '"';
        const searchResults = cordra.search(query).results;
        for (const r of searchResults) {
            if (r.content[USER_OAUTH_PROP] === payload.sub && r.content.accountActive) {
                result.userId = r.id;
                result.username = r.content.username;
                if (payload.exp) {
                    result.exp = payload.exp;
                }
                result.grantAuthenticatedAccess = true;
                return result;
            }
        }
    }
    return result;
}

function checkClaims(claims) {
    if (!claims.iss || !claims.exp || !claims.aud) {
        return false;
    }
    if (TOKEN_ISS !== claims.iss) {
        return false;
    }
    const nowInSeconds = Math.floor(Date.now() / 1000);
    if (nowInSeconds > claims.exp) {
        return false;
    }
    const aud = claims.aud;
    if (!checkAudience(aud)) {
        return false;
    }
    return true;
}

function checkAudience(audElement) {
    let aud = [];
    if (typeof audElement === "string") {
        aud.push(audElement);
    } else if (Array.isArray(audElement)) {
        aud = audElement;
    } else {
        return false;
    }
    if (aud.includes(TOKEN_AUD)) {
        return true;
    } else {
        return false;
    }
}

function cacheKeyIfNeeded() {
    if (!providerPublicKey) {
        const configDir = getDataDir();
        const File = Java.type('java.io.File');
        const keyPath = configDir + File.separator + "publicKey.jwk";
        providerPublicKey = readFileToJsonAndParse(keyPath);
    }
}

function getDataDir() {
    const System = Java.type('java.lang.System');
    const cordraDataDir = System.getProperty('cordra.data');
    return cordraDataDir;
}

function readFileToString(pathToFile) {
    const path = Java.type('java.nio.file.Paths').get(pathToFile);
    const string = Java.type('java.nio.file.Files').readString(path);
    return string;
}

function readFileToJsonAndParse(pathToFile) {
    const jsonString = readFileToString(pathToFile);
    const result = JSON.parse(jsonString);
    return result;
}