function findNextTabStop(el: any) {
  var universe = document.querySelectorAll(
    'input, button, select, textarea, a[href]'
  );
  var list = Array.prototype.filter.call(universe, function (item) {
    return item.tabIndex >= '0';
  });
  var index = list.indexOf(el);
  return list[index + 1] || list[0];
}

export function handleEnterAsTabToNext(event: any, isPreventDefault?: boolean) {
  if (event.keyCode === 13) {
    findNextTabStop(event.target).focus();
    if (isPreventDefault ?? true) {
      event.preventDefault();
    }
  }
}
