import { forumServiceClient, TaggedThreadFields } from "./forum.client.ts";
import { ListResponse } from "../client.ts";

export async function requestGetThreadTags(threadId: number | string) {
  const { data } = await forumServiceClient.get<
    ListResponse<TaggedThreadFields>
  >(`models/tagged-threads/records/?thread=${threadId}`);
  return data;
}

export const threadTagsQueryKey = ["thread-tags"];
