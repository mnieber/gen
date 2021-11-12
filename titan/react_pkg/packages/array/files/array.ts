export function removeItemsFromArray(arr: any[], values: any[]) {
  var i = 0;
  while (i < arr.length) {
    if (values.includes(arr[i])) {
      arr.splice(i, 1);
    } else {
      ++i;
    }
  }
  return arr;
}
