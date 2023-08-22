import { AUTH_LOCALSTORAGE_KEY } from "../client.ts";
import { accountServiceClient } from "./account.client.ts";
import { Model } from "../client.ts";
import { AccountFields } from "./account.client.ts";

export async function requestChangePassword({
  oldPassword,
  newPassword,
}: {
  oldPassword: string;
  newPassword: string;
}) {
  const { data } = await accountServiceClient.post<Model<AccountFields>>(
    "/models/users/change-password/",
    {
      old_password: oldPassword,
      new_password1: newPassword,
      new_password2: newPassword,
    }
  );

  if (localStorage.getItem(AUTH_LOCALSTORAGE_KEY)) {
  }

  return data;
}
