import { accountServiceClient } from "./account.client.ts";
import { AUTH_LOCALSTORAGE_KEY } from "../client.ts";

export async function requestLogin({
  username,
  password,
}: {
  username: string;
  password: string;
}) {
  const { data } = await accountServiceClient.post<{ token: string }>(
    "/models/users/login/",
    {
      username,
      password,
    },
  );
  localStorage.setItem(AUTH_LOCALSTORAGE_KEY, data.token);
}
