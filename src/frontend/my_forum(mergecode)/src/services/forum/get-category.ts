import { forumServiceClient, CategoryFields } from "./forum.client.ts";
import { ListResponse } from "../client.ts";

export async function requestGetCategory(threadId: number | string) {
  const { data } = await forumServiceClient.get<ListResponse<CategoryFields>>(
    `models/thread-categories/records/?thread=${threadId}`
  );
  return data;
}
