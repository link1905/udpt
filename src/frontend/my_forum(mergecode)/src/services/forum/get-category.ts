import { forumServiceClient, CategoryFields } from "./forum.client.ts";
import { Model } from "../client.ts";

export async function requestGetCategory(threadId: number | string) {
  const { data } = await forumServiceClient.get<Model<CategoryFields>>(
    `models/thread-categories/records/?thread=${threadId}`
  );
  return data;
}
