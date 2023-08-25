import { Model } from "../client.ts";
import { forumServiceClient, ThreadFields } from "./forum.client.ts";

export const requestGetThread = (id: string) =>
  forumServiceClient
    .get<Model<ThreadFields>>(`/models/threads/records/${id}/`)
    .then((res) => res.data);

export const getThreadQueryKey = (pk: string | number) => ["thread", pk];
