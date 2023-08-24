import {
  forumServiceClient,
  ThreadFields,
} from "./forum.client.ts";
import { Model } from "../client.ts";

export const requestDeleteThreadVote = (id: string | number) =>
  forumServiceClient
    .delete<Model<ThreadFields>>(`/models/thread-votes/records/${id}/`)
    .then((res) => res.data);
