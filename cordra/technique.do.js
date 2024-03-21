const cordra = require('cordra');
const schema = require('/cordra/schemas/Technique.schema.json');

exports.beforeSchemaValidation = beforeSchemaValidation;

function beforeSchemaValidation(object, context) {
    object.content.$schema = schema.$id;
    
    // get the preferred label for the technique
    const controlledListSchema = require('/cordra/schemas/Controlled lists.schema.json');
    const cl_enum = controlledListSchema.definitions.technique.enum;
    const cl_titles = controlledListSchema.definitions.technique.options.enum_titles;

    let index = cl_enum.indexOf(object.content.e-rihs_vocab_id);
    if (index > -1) {
        object.content.preferred_label = cl_titles[index];
    } else {
        object.content.preferred_label = "[untitled technique]";
    } 

    return object;
}