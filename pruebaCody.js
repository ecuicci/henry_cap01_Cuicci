function suma(a, b) {
    return a + b;
}

/**
 * Sorts the given array in ascending order.
 * @param {Array} array - The array to be sorted.
 * @returns {Array} The sorted array.
 */
function ordenarArray(array) {
    return array.sort();
}

//necesito una función que reciba un array de números y devuelva el promedio
function promedio(array) {
    let suma = 0;
    for (let i = 0; i < array.length; i++) {
        suma += array[i];
    }
    return suma / array.length;
}