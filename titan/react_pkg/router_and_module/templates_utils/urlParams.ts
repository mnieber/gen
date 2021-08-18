export const searchParams = () => new URLSearchParams(window.location.search);
export const getNextUrl = (defaultUrl: string) =>
  searchParams().get('next') ?? defaultUrl;
