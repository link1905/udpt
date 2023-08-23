import { accountServiceClient } from "./account.client.ts";

export async function requestGetDetailAccount(pk: number) {
  const { data } = await accountServiceClient.get(
    `/models/users/records/${pk}/`
  );
  return data;
}
