import { AccountFields, accountServiceClient } from "./account.client.ts";
import { AUTH_LOCALSTORAGE_KEY, Model } from "../client.ts";

export async function requestAuthRefresh() {
  const { data } = await accountServiceClient.post<{
    token: string;
    user: Model<AccountFields>;
  }>("/models/users/auth-refresh/", {});
  localStorage.setItem(AUTH_LOCALSTORAGE_KEY, data.token);
  return data.user;
}

export const authRequestQueryKey = ["auth"];
