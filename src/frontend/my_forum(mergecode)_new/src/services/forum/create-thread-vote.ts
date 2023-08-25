import {
  CreateThreadVoteData,
  forumServiceClient,
  ThreadFields,
} from "./forum.client.ts";
import { Model } from "../client.ts";

export const requestCreateThreadVote = (data: CreateThreadVoteData) =>
  forumServiceClient
    .post<Model<ThreadFields>>("/models/thread-votes/records/", data)
    .then((res) => res.data);
