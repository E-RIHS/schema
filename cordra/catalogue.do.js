const cordra = require('cordra');
const schema = require('/cordra/schemas/Catalogue.schema.json');

exports.beforeSchemaValidation = beforeSchemaValidation;

function beforeSchemaValidation(object, context) {
    object.content.$schema = schema.$id;
    return object;
}