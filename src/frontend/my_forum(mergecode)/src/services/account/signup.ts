import { accountServiceClient } from "./account.client.ts";
import { AUTH_LOCALSTORAGE_KEY } from "../client.ts";

export async function requestSignUp({
  username,
  password1,
  password2,
  email,
  first_name,
  last_name,
}: {
  username: string;
  password1: string;
  password2: string;
  email: string;
  first_name: string;
  last_name: string;
}) {
  const { data } = await accountServiceClient.post<{ token: string }>(
    "/models/users/records/",
    {
      username,
      password1,
      password2,
      email,
      first_name,
      last_name,
    }
  );
  localStorage.setItem(AUTH_LOCALSTORAGE_KEY, data.token);
}
  