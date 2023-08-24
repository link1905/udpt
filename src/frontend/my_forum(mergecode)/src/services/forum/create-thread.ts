import { Model } from "../client.ts";
import {
  forumServiceClient,
  CreateThreadForm,
  ThreadFields,
} from "./forum.client.ts";

export const requestCreateThread = (data: CreateThreadForm) =>
  forumServiceClient
    .post<Model<ThreadFields>>("/models/threads/records/", data)
    .then((res) => res.data);
