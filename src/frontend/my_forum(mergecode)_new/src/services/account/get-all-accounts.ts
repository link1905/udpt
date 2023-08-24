import { accountServiceClient, AccountFields } from "./account.client.ts";

export async function requestGetAllAccounts() {
  const response = await accountServiceClient.get("/models/users/records/");
  return response.data.results as AccountFields[];
}
