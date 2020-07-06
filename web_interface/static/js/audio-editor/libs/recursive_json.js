const stringifyJSON = data => {
  if (data === undefined)
    return undefined
  else if (data === null)
    return 'null'
  else if (data.constructor === String)
    return '"' + data.replace(/"/g, '\\"') + '"'
  else if (data.constructor === Number)
    return String(data)
  else if (data.constructor === Boolean)
    return data ? 'true' : 'false'
  else if (data.constructor === Array)
    return '[ ' + data.reduce((acc, v) => {
      if (v === undefined)
        return [...acc, 'null']
      else
        return [...acc, stringifyJSON(v)]
    }, []).join(', ') + ' ]'
  else if (data.constructor === Object)
    return '{ ' + Object.keys(data).reduce((acc, k) => {
      if (data[k] === undefined)
        return acc
      else
        return [...acc, stringifyJSON(k) + ':' + stringifyJSON(data[k])]
    }, []).join(', ') + ' }'
  else
    return '{}'
}

// round-trip test and log to console
const test = data => {
  return console.log(stringifyJSON(data));
}

test(null)                               // null
test('he said "hello"')                  // 'he said "hello"'
test(5)                                  // 5
test([1,2,true,false])                   // [ 1, 2, true, false ]
test({a:1, b:2})                         // { a: 1, b: 2 }
test([{a:1},{b:2},{c:3}])                // [ { a: 1 }, { b: 2 }, { c: 3 } ]
test({a:[1,2,3], c:[4,5,6]})             // { a: [ 1, 2, 3 ], c: [ 4, 5, 6 ] }
test({a:undefined, b:2})                 // { b: 2 }
test({[undefined]: 1})                   // { undefined: 1 }
test([[["test","mike",4,["jake"]],3,4]]) // [ [ [ 'test', 'mike', 4, [ 'jake' ] ], 3, 4 ] ]
