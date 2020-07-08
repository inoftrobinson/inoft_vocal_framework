function deepstringify(sourceObject) {
    let newe = {};
    for (key in sourceObject) {
        let currentObject = sourceObject[key];
        console.log(key);
        if (typeof currentObject == "object") {
            newe[key] = deepstringify(currentObject);
        } else {
            newe[key] = JSON.stringify(currentObject);
        }
    }
    return newe;
}