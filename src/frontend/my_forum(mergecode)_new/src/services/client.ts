import { CreateAxiosDefaults } from "axios";

export const AUTH_LOCALSTORAGE_KEY = "AUTH_LOCALSTORAGE";

export function createAxiosConfig(pathname: string): CreateAxiosDefaults {
  const url = new URL(import.meta.env.VITE_API_URL ?? "/");
  url.pathname = pathname;
  return {
    baseURL: url.toString(),
    headers: {
      Authorization: {
        toString() {
          return localStorage.getItem(AUTH_LOCALSTORAGE_KEY);
        },
      } as string,
    },
  };
}

export interface ListResponse<T> {
  count: number;
  results: Model<T>[];
}

export interface Model<T> {
  pk: number;
  model: "taggit.tag";
  fields: T;
  path: string;
}
