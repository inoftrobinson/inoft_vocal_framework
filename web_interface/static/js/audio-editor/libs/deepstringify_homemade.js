function deepstringify(sourceObject) {
    var newe = {};
    for (key in sourceObject) {
        console.log(key);
        if (typeof sourceObject[key] == "object") {
            newe[key] = deepstringify(sourceObject[key]);
        } else {
            newe[key] = JSON.stringify(sourceObject[key]);
        }
    }
    return newe;
}