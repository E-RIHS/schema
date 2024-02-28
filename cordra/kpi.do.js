const cordra = require('cordra');
const schema = require('/cordra/schemas/KPI.schema.json');

exports.beforeSchemaValidation = beforeSchemaValidation;

function beforeSchemaValidation(object, context) {
    object.content.$schema = schema.$id;
    
    // // Possible self-contained solution to calculate a KPI score
    // // see https://www.freecodecamp.org/news/how-to-use-the-javascript-require-function/
    // // (Not sure how this would work if it needs to pull data from an external source with authorization)
    // let kpiDef = object.content.kpi_definition;
    // const calc = require('/#objects/' + kpiDef + '?payload=calc.js');
    // object.content.metrics = calcKpi(object.content.date_range);
    // // ..
    
    return object;
}