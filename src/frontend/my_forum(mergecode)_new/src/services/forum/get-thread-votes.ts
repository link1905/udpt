import { forumServiceClient, ThreadVoteFields } from "./forum.client.ts";
import { ListResponse } from "../client.ts";

export async function requestGetThreadVotes(threadId: number | string) {
  const { data } = await forumServiceClient.get<ListResponse<ThreadVoteFields>>(
    `models/thread-votes/records/?thread=${threadId}`,
  );
  return data;
}
export const getThreadVotesKey = (threadId: number | string) => [
  "thread-votes",
  String(threadId),
];
