export function handleEnterAsTabToNext(event: any, isPreventDefault: boolean) {
  const form = event.target.form;
  if (form && event.keyCode === 13) {
    const index = Array.prototype.indexOf.call(form, event.target);
    form.elements[index + 1].focus();
    if (isPreventDefault) {
      event.preventDefault();
    }
  }
}

