const cordra = require('cordra');
exports.beforeSchemaValidation = beforeSchemaValidation;


async function getControlledList(url) {
    // there is not built-in support for fetch.  Currently you'd need to use Java to make HTTP calls
    // see: https://www.baeldung.com/java-9-http-client
    const HttpClient = Java.type('java.net.http.HttpClient');
    const HttpRequest = Java.type('java.net.http.HttpRequest');
    const HttpResponse = Java.type('java.net.http.HttpResponse');
    const URI = Java.type('java.net.URI');
    const client = HttpClient.newBuilder().build();
    const request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build();
    const response = client.send(request, HttpResponse.BodyHandlers.ofString());
    // if valid response, return the controlled list
    if (response.statusCode() === 200) {
        const body = JSON.parse(response.body());
        if (Object.keys(body.list).length > 0) {
            return body.list;
        }
    }
    // if anything goes wrong
    throw new Error('Invalid response from ' + url);
}


async function beforeSchemaValidation(object, context) {
    // update controlled list enums with external data
    if (object.content.name === 'Controlled lists') {
        for (const cl in object.content.schema.definitions) {
            const definition = object.content.schema.definitions[cl];
            const url = definition['e-rihs'].enum_source;
            const list = await getControlledList(url);
            if (list) {
                let terms = Object.keys(list);
                let labels = Object.values(list);
                definition.enum = terms;
                if (!('options' in definition)) {
                    definition.options = {};
                }
                definition.options.enum_titles = labels;
            }
        }
    }
    return object;
}