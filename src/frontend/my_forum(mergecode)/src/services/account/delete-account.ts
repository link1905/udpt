import { accountServiceClient } from "./account.client.ts";

export async function requestDeleteAccount(pk: number) {
  const response = await accountServiceClient.delete(
    `/models/users/records/${pk}/`
  );
  return response.data;
}
