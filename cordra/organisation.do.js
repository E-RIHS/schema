const cordra = require('cordra');
const schema = require('/cordra/schemas/Organisation.schema.json');

exports.beforeSchemaValidation = beforeSchemaValidation;

function beforeSchemaValidation(object, context) {
    object.content.$schema = schema.$id;
    object.content.display_name = object.content.name + ' (' + object.content.acronym + ')';
    return object;
}