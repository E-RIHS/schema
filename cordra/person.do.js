const cordra = require('cordra');
const schema = require('/cordra/schemas/Person.schema.json');

exports.beforeSchemaValidation = beforeSchemaValidation;

function beforeSchemaValidation(object, context) {
    object.content.$schema = schema.$id;
    object.content.full_name = object.content.last_name + ', ' + object.content.first_name;
    return object;
}