import { ListResponse } from "../client.ts";
import { forumServiceClient, ThreadFields } from "./forum.client.ts";

export const requestGetAllThreads = (parent: string | number) =>
  forumServiceClient
    .get<ListResponse<ThreadFields>>(
      `/models/threads/records/` + (parent ? `?parent=${parent}` : ""),
    )
    .then((res) => res.data);

export const getAllThreadsQueryKey = (parent: string | number) =>
  parent ? ["thread", parent, "child"] : ["thread"];
