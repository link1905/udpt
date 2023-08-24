import {AccountFields, accountServiceClient} from "./account.client.ts";
import {Model} from "../client.ts";

export async function requestGetDetailAccount(pk: number) {
  const { data } = await accountServiceClient.get<Model<AccountFields>>(
    `/models/users/records/${pk}/`,
  );
  return data;
}

export const requestGetDetailAccountKeys = (pk: number) => ["account", pk];
